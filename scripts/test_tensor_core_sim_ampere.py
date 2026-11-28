#!/usr/bin/env python3
"""对拍：Ampere 模拟器（nvidia_tensor_core_sim_ampere.html）vs MMASim / math.fma。

用法：
    pip install torch mmasim
    python scripts/test_tensor_core_sim_ampere.py [每模式用例数，默认 300]

脚本从 HTML 里抽出 <script id="model"> 的模型，用 Node 跑模拟器的 ampDot，
再用 MMASim 的 Ampere 参数算同一个矩阵乘：

    FP16→FP32 : F=24, L=8, RZ-FP32
    FP16→FP16 : F=24, L=8, RNE-FP16
    BF16→FP32 : F=24, L=8, RZ-FP32
    TF32→FP32 : F=24, L=4, RZ-FP32（k=8 分两次对齐）
    FP64→FP64 : IEEE-754 FMA 链（用 math.fma 做参考实现）

另外对拍输入舍入（RNE 到 FP16/BF16、截断到 TF32）。
"""

import json
import math
import os
import random
import re
import shutil
import struct
import subprocess
import sys
import tempfile

import torch

from mmasim.arithmetic.fdpa import MMA_T_FDPA

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "docs", "hardware", "nvidia_tensor_core_sim_ampere.html")

# m×n×k 是模拟器画出来的“每周期”tile
MODES = {
    "f16f32": dict(op=MMA_T_FDPA(24, "RZ-FP32", 8, -132, "f16", "f16"), m=8, n=4, k=8, dtype=torch.float16, out="f32"),
    "f16f16": dict(op=MMA_T_FDPA(24, "RNE-FP16", 8, -20, "f16", "f16"), m=8, n=4, k=8, dtype=torch.float16, out="f16"),
    "bf16f32": dict(op=MMA_T_FDPA(24, "RZ-FP32", 8, -132, "bf16", "bf16"), m=8, n=4, k=8, dtype=torch.bfloat16, out="f32"),
    "tf32f32": dict(op=MMA_T_FDPA(24, "RZ-FP32", 4, -132, "tf32", "tf32"), m=8, n=4, k=4, dtype=torch.float32, out="f32"),
}
F64_M, F64_N, F64_K = 2, 2, 4


F16_MAX = 65504.0
F32_MAX = 1e37


def clamp(x, lim):
    if x != x:
        return 0.0
    return max(-lim, min(lim, x))


def f32of(x):
    return struct.unpack("<f", struct.pack("<f", clamp(x, F32_MAX)))[0]


def f16(x):
    return float(torch.tensor(f32of(clamp(x, F16_MAX)), dtype=torch.float16))


def bf16(x):
    return float(torch.tensor(f32of(x), dtype=torch.bfloat16))


def tf32(x):
    b = struct.unpack("<I", struct.pack("<f", f32of(x)))[0]
    return struct.unpack("<f", struct.pack("<I", b & 0xFFFFE000))[0]


def bits_f32(x):
    return struct.unpack("<I", struct.pack("<f", float(x)))[0]


def bits_f16(x):
    return struct.unpack("<H", struct.pack("<e", float(x)))[0]


def bits_f64(x):
    return struct.unpack("<Q", struct.pack("<d", float(x)))[0]


def log_uniform(rng, lo, hi):
    return rng.uniform(-1, 1) * 2 ** rng.uniform(lo, hi)


def gen_case(rng, kind, quant, m, n, k, cquant):
    def val(lo, hi):
        return quant(log_uniform(rng, lo, hi))

    if kind == 0:  # 普通
        A = [[val(-4, 4) for _ in range(k)] for _ in range(m)]
        B = [[val(-4, 4) for _ in range(n)] for _ in range(k)]
        C = [[cquant(rng.gauss(0, 1)) for _ in range(n)] for _ in range(m)]
    elif kind == 1:  # 宽动态范围
        A = [[val(-30, 30) for _ in range(k)] for _ in range(m)]
        B = [[val(-30, 30) for _ in range(n)] for _ in range(k)]
        C = [[cquant(log_uniform(rng, -60, 60)) for _ in range(n)] for _ in range(m)]
    elif kind == 2:  # 稀疏 / 零
        A = [[quant(rng.choice([0.0, 0.0, log_uniform(rng, -6, 6)])) for _ in range(k)] for _ in range(m)]
        B = [[quant(rng.choice([0.0, 0.0, log_uniform(rng, -6, 6)])) for _ in range(n)] for _ in range(k)]
        C = [[cquant(rng.choice([0.0, log_uniform(rng, -8, 8)])) for _ in range(n)] for _ in range(m)]
    elif kind == 3:  # 抵消
        A = [[quant(1.0) for _ in range(k)] for _ in range(m)]
        B = [[quant(rng.choice([-1, 1]) * rng.random()) for _ in range(n)] for _ in range(k)]
        C = [[cquant(-sum(A[i][q] * B[q][j] for q in range(k)) * (1 + rng.uniform(-1e-4, 1e-4)))
              for j in range(n)] for i in range(m)]
    else:  # 一行大、一行小：专门压截断位
        A = [[quant(rng.choice([1.0, 2 ** -24, 2 ** -25, 2 ** -26, 0.0])) for _ in range(k)] for _ in range(m)]
        B = [[quant(1.0) for _ in range(n)] for _ in range(k)]
        C = [[cquant(rng.choice([1.0, 0.0, 2 ** -24])) for _ in range(n)] for _ in range(m)]
    return A, B, C


NODE_RUNNER = r"""
const fs = require('fs');
const M = require(process.argv[2]);
const cases = JSON.parse(fs.readFileSync(process.argv[3]));
const modes = ['f16f32', 'f16f16', 'bf16f32', 'tf32f32', 'f64f64'];

const b32 = new DataView(new ArrayBuffer(4));
function bitsF32(x) { b32.setFloat32(0, x); return b32.getUint32(0); }
function bitsF16(v) { const t = new Float32Array(1); t[0] = v; return f16raw(v); }
function f16raw(v) {
  if (Number.isNaN(v)) return 0x7e00;
  if (!isFinite(v)) return v > 0 ? 0x7c00 : 0xfc00;
  if (v === 0) return Object.is(v, -0) ? 0x8000 : 0;
  const sign = v < 0 ? 0x8000 : 0;
  const a = Math.abs(v);
  let e = Math.floor(Math.log2(a));
  if (Math.pow(2, e) > a) e--;
  if (Math.pow(2, e + 1) <= a) e++;
  if (e < -14) return sign | Math.round(a / Math.pow(2, -24));
  const m = a / Math.pow(2, e - 10);
  return sign | ((e + 15) << 10) | (Math.round(m - 1024) & 0x3ff);
}
const b64 = new DataView(new ArrayBuffer(8));
function bitsF64(x) {
  b64.setFloat64(0, x);
  return b64.getBigUint64(0).toString();
}

const out = [];
for (const c of cases) {
  const rec = {};
  for (const mode of [c.mode]) {
    const d = [];
    for (let i = 0; i < c.m; i++) {
      const row = [];
      for (let j = 0; j < c.n; j++) {
        const v = M.ampDot(c.A, c.B, c.C, i, j, mode).d;
        row.push(mode === 'f16f16' ? f16raw(v) : mode === 'f64f64' ? bitsF64(v) : bitsF32(v));
      }
      d.push(row);
    }
    rec[mode] = d;
  }
  out.push(rec);
}
process.stdout.write(JSON.stringify(out));
"""

ROUND_RUNNER = r"""
const fs = require('fs');
const M = require(process.argv[2]);
const vals = JSON.parse(fs.readFileSync(process.argv[3]));
const out = { f16: [], bf16: [], tf32: [] };
const b32 = new DataView(new ArrayBuffer(4));
function bitsF32(x) { b32.setFloat32(0, x); return b32.getUint32(0); }
for (const v of vals) {
  out.f16.push(bitsF32(M.quantize(v, 'f16')));
  out.bf16.push(bitsF32(M.quantize(v, 'bf16')));
  out.tf32.push(bitsF32(M.quantize(v, 'tf32')));
}
process.stdout.write(JSON.stringify(out));
"""


def f64_reference(cases):
    """用 math.fma 做 FP64 链的参考实现（需要 Python 3.13+）。"""
    code = r"""
import json, math, struct, sys
cases = json.load(sys.stdin)
out = []
for A, B, C in cases:
    m, n = len(C), len(C[0])
    rows = []
    for i in range(m):
        row = []
        for j in range(n):
            acc = C[i][j]
            for q in range(len(A[0])):
                acc = math.fma(A[i][q], B[q][j], acc)
            row.append(struct.unpack("<Q", struct.pack("<d", acc))[0])
        rows.append(row)
    out.append(rows)
json.dump(out, sys.stdout)
"""
    for exe in (sys.executable, shutil.which("python3")):
        if not exe:
            continue
        try:
            r = subprocess.run([exe, "-c", "import math,sys; sys.exit(0 if hasattr(math,'fma') else 1)"],
                               capture_output=True)
            if r.returncode != 0:
                continue
            r = subprocess.run([exe, "-c", code], input=json.dumps(cases),
                               capture_output=True, text=True, check=True)
            return json.loads(r.stdout)
        except Exception:
            continue
    return None


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    node = shutil.which("node")
    if node is None:
        sys.exit("需要 node（用于运行模拟器的 JS 模型）")

    html = open(HTML, encoding="utf-8").read()
    m = re.search(r'<script id="model">(.*?)</script>', html, re.S)
    if not m:
        sys.exit('在 HTML 中找不到 <script id="model">')

    tmp = tempfile.mkdtemp(prefix="ampere-sim-")
    model_path = os.path.join(tmp, "model.js")
    with open(model_path, "w", encoding="utf-8") as f:
        f.write(m.group(1))
    runner_path = os.path.join(tmp, "runner.js")
    with open(runner_path, "w", encoding="utf-8") as f:
        f.write(NODE_RUNNER)
    round_path = os.path.join(tmp, "round.js")
    with open(round_path, "w", encoding="utf-8") as f:
        f.write(ROUND_RUNNER)

    rng = random.Random(20261119)

    QUANT = {
        "f16": f16,
        "bf16": bf16,
        "tf32": tf32,
    }

    cases = []
    for kind in range(5):
        for _ in range(n):
            mode = rng.choice(list(MODES))
            q = QUANT["tf32" if mode == "tf32f32" else ("bf16" if mode == "bf16f32" else "f16")]
            cq = f16 if mode == "f16f16" else tf32
            info = MODES[mode]
            A, B, C = gen_case(rng, kind, q, info["m"], info["n"], info["k"], cq)
            cases.append({"mode": mode, "m": info["m"], "n": info["n"], "A": A, "B": B, "C": C})

    # FP64 用例（单独一组，A/B/C 是普通 double）
    f64_cases = []
    for kind in range(5):
        for _ in range(n):
            A = [[log_uniform(rng, -20, 20) for _ in range(F64_K)] for _ in range(F64_M)]
            B = [[log_uniform(rng, -20, 20) for _ in range(F64_N)] for _ in range(F64_K)]
            C = [[log_uniform(rng, -40, 40) for _ in range(F64_N)] for _ in range(F64_M)]
            if kind == 3:
                C = [[-sum(A[i][q] * B[q][j] for q in range(F64_K)) * (1 + rng.uniform(-1e-12, 1e-12))
                      for j in range(F64_N)] for i in range(F64_M)]
            f64_cases.append({"mode": "f64f64", "m": F64_M, "n": F64_N, "A": A, "B": B, "C": C})

    payload = [{"mode": c["mode"], "A": c["A"], "B": c["B"], "C": c["C"], "m": c["m"], "n": c["n"]}
               for c in cases + f64_cases]
    payload_path = os.path.join(tmp, "cases.json")
    with open(payload_path, "w", encoding="utf-8") as f:
        json.dump(payload, f)

    r = subprocess.run([node, runner_path, model_path, payload_path],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("node 运行失败：\n" + r.stderr)
    got = json.loads(r.stdout)

    total = 0
    bad = 0

    def check(label, want, have, case, extra=""):
        nonlocal total, bad
        total += 1
        if want != have:
            bad += 1
            if bad <= 8:
                print(f"mismatch {label} got {have} want {want} {extra}")

    # MMASim 参考
    for idx, c in enumerate(cases):
        mode = c["mode"]
        info = MODES[mode]
        k = info["k"]
        n = info["n"]
        A = torch.tensor([row[:k] for row in c["A"]], dtype=info["dtype"])
        B = torch.tensor([row[:n] for row in c["B"][:k]], dtype=info["dtype"])
        C = torch.tensor(c["C"], dtype=torch.float16 if mode == "f16f16" else torch.float32)
        d = info["op"](A, B, C)
        for i in range(info["m"]):
            for j in range(info["n"]):
                v = d[i][j].item()
                want = bits_f16(v) if info["out"] == "f16" else bits_f32(v)
                check(mode, want, got[idx][mode][i][j], c, f"[{i}][{j}]")

    # FP64 参考
    ref64 = f64_reference([[c["A"], c["B"], c["C"]] for c in f64_cases])
    if ref64 is None:
        print("跳过 FP64（找不到带 math.fma 的 Python）")
    else:
        base = len(cases)
        for idx in range(len(f64_cases)):
            for i in range(F64_M):
                for j in range(F64_N):
                    want = ref64[idx][i][j]
                    have = int(got[base + idx]["f64f64"][i][j])
                    check("f64f64", want, have, f64_cases[idx], f"[{i}][{j}]")

    # 输入舍入
    vals = [log_uniform(rng, -30, 30) for _ in range(2000)] + [0.0, 1.0, -1.0, 65504, 1e-8, 1e-40]
    vals_path = os.path.join(tmp, "vals.json")
    with open(vals_path, "w", encoding="utf-8") as f:
        json.dump(vals, f)
    r = subprocess.run([node, round_path, model_path, vals_path], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("node 运行失败：\n" + r.stderr)
    rr = json.loads(r.stdout)
    rbad = 0
    rchecked = 0
    for i, v in enumerate(vals):
        # 超出格式范围的值两边处理不同（这里只比可表示范围内的输入）
        if abs(v) <= F16_MAX:
            rchecked += 1
            if rr["f16"][i] != bits_f32(f16(v)):
                rbad += 1
                if rbad <= 5:
                    print("rounding mismatch f16", repr(v), hex(rr["f16"][i]), hex(bits_f32(f16(v))))
        if abs(v) <= F32_MAX:
            rchecked += 2
            if rr["bf16"][i] != bits_f32(bf16(v)):
                rbad += 1
                if rbad <= 5:
                    print("rounding mismatch bf16", repr(v), hex(rr["bf16"][i]), hex(bits_f32(bf16(v))))
            if rr["tf32"][i] != bits_f32(tf32(v)):
                rbad += 1
                if rbad <= 5:
                    print("rounding mismatch tf32", repr(v), hex(rr["tf32"][i]), hex(bits_f32(tf32(v))))
    print(f"compared {total} outputs, {bad} mismatches; rounding: {rchecked} checks, {rbad} mismatches")
    shutil.rmtree(tmp, ignore_errors=True)
    sys.exit(1 if bad or rbad else 0)


if __name__ == "__main__":
    main()
