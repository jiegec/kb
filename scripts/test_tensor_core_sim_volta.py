#!/usr/bin/env python3
"""对拍：Volta 模拟器（nvidia_tensor_core_sim_volta.html）里的 JS 模型 vs MMASim。

用法：
    pip install torch mmasim
    python scripts/test_tensor_core_sim_volta.py [case 数，默认 500]

脚本会从 HTML 中抽出 <script id="model"> 的模型代码，用 Node 跑模拟器的
voltaDot4，并用 MMASim 的 Volta 配置算同一个 4x4x4，逐位比较 16 个输出。
覆盖 FP32（RZ）和 FP16（RNE）两种输出格式。
"""

import json
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
HTML = os.path.join(ROOT, "docs", "hardware", "nvidia_tensor_core_sim_volta.html")

OP32 = MMA_T_FDPA(23, "RZ-FP32", 4, -131, "f16", "f16")
OP16 = MMA_T_FDPA(23, "RNE-FP16", 4, -19, "f16", "f16")


def f16(x):
    return float(torch.tensor(x, dtype=torch.float16))


def f32(x):
    return float(torch.tensor(x, dtype=torch.float32))


def bits32(x):
    return struct.unpack("<I", struct.pack("<f", float(x)))[0]


def bits16(x):
    return struct.unpack("<H", struct.pack("<e", float(x)))[0]


def log_uniform(rng, lo, hi):
    return rng.uniform(-1, 1) * 2 ** rng.uniform(lo, hi)


def gen_case(rng, kind):
    if kind == 0:
        A = [[rng.gauss(0, 1) for _ in range(4)] for _ in range(4)]
        B = [[rng.gauss(0, 1) for _ in range(4)] for _ in range(4)]
        C = [[rng.gauss(0, 1) for _ in range(4)] for _ in range(4)]
    elif kind == 1:
        A = [[log_uniform(rng, -20, 15) for _ in range(4)] for _ in range(4)]
        B = [[log_uniform(rng, -20, 15) for _ in range(4)] for _ in range(4)]
        C = [[log_uniform(rng, -100, 100) for _ in range(4)] for _ in range(4)]
    elif kind == 2:  # 次正规输入
        A = [[rng.uniform(-1, 1) * 2 ** -24 for _ in range(4)] for _ in range(4)]
        B = [[log_uniform(rng, -14, 14) for _ in range(4)] for _ in range(4)]
        C = [[log_uniform(rng, -120, -100) for _ in range(4)] for _ in range(4)]
    elif kind == 3:  # 抵消
        A = [[1.0] * 4 for _ in range(4)]
        B = [[rng.choice([-1, 1]) * rng.random() for _ in range(4)] for _ in range(4)]
        C = [[-sum(A[i][k] * B[k][j] for k in range(4)) * (1 + rng.uniform(-1e-6, 1e-6))
              for j in range(4)] for i in range(4)]
    elif kind == 4:  # 稀疏 / 零
        A = [[rng.choice([0.0, 0.0, 0.0, f16(rng.gauss(0, 2))]) for _ in range(4)] for _ in range(4)]
        B = [[rng.choice([0.0, 0.0, 0.0, f16(rng.gauss(0, 2))]) for _ in range(4)] for _ in range(4)]
        C = [[rng.choice([0.0, 0.0, f16(rng.gauss(0, 2))]) for _ in range(4)] for _ in range(4)]
    else:  # 接近 FP16 上限，触发 FP16 输出溢出
        A = [[rng.choice([-1, 1]) * rng.uniform(3e4, 6.5e4) for _ in range(4)] for _ in range(4)]
        B = [[rng.choice([-1, 1]) * rng.uniform(0.5, 2.0) for _ in range(4)] for _ in range(4)]
        C = [[rng.choice([-1, 1]) * rng.uniform(0, 6e4) for _ in range(4)] for _ in range(4)]
    return A, B, C


def make_case(A, B, C):
    A = [[f16(x) for x in row] for row in A]
    B = [[f16(x) for x in row] for row in B]
    C32 = [[f32(x) for x in row] for row in C]
    C16 = [[f16(x) for x in row] for row in C]
    if any(not (abs(x) < 3.4e38) for row in C32 for x in row):
        return None
    if any(not (abs(x) < 65504) for row in C16 for x in row):
        return None  # C 超出 FP16 范围，模拟器 UI 会钳位，不参与本对拍

    tA = torch.tensor(A, dtype=torch.float16)
    tB = torch.tensor(B, dtype=torch.float16)
    d32 = OP32(tA, tB, torch.tensor(C32, dtype=torch.float32))
    d16 = OP16(tA, tB, torch.tensor(C16, dtype=torch.float16))
    return {
        "A": A,
        "B": B,
        "C32": C32,
        "C16": C16,
        "D32": [[bits32(d32[i][j].item()) for j in range(4)] for i in range(4)],
        "D16": [[bits16(d16[i][j].item()) for j in range(4)] for i in range(4)],
    }


NODE_RUNNER = r"""
const fs = require('fs');
const M = require(process.argv[2]);
const cases = JSON.parse(fs.readFileSync(process.argv[3]));
const rounding = JSON.parse(fs.readFileSync(process.argv[4]));

function f32bits(x) {
  const b = new ArrayBuffer(4);
  new DataView(b).setFloat32(0, x);
  return new DataView(b).getUint32(0);
}

function f16bits(v) {
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
  return sign | ((e + 15) << 10) | Math.round(m - 1024);
}

let bad = 0, total = 0;
for (const c of cases) {
  for (const fmt of ['f32', 'f16']) {
    const C = fmt === 'f32' ? c.C32 : c.C16;
    const want = fmt === 'f32' ? c.D32 : c.D16;
    for (let i = 0; i < 4; i++) {
      for (let j = 0; j < 4; j++) {
        total++;
        const r = M.voltaDot4(c.A, c.B, C, i, j, fmt);
        const got = fmt === 'f32' ? f32bits(r.d) : f16bits(r.d);
        if (got !== want[i][j]) {
          bad++;
          if (bad <= 5) {
            console.log('mismatch', fmt, i, j, 'got', got.toString(16), 'want', want[i][j].toString(16));
            console.log(JSON.stringify({ a: c.A[i], b: c.B.map(row => row[j]), c: C[i][j] }));
          }
        }
      }
    }
  }
}
let rbad = 0;
for (const r of rounding) {
  if (f16bits(M.rneF16(r.x)) !== r.h) rbad++;
  if (f32bits(Math.fround(r.x)) !== r.f) rbad++;
}
console.log(`compared ${total} outputs, ${bad} mismatches; rounding: ${rounding.length * 2} checks, ${rbad} mismatches`);
process.exit(bad || rbad ? 1 : 0);
"""


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    node = shutil.which("node")
    if node is None:
        sys.exit("需要 node（用于运行模拟器的 JS 模型）")

    html = open(HTML, encoding="utf-8").read()
    m = re.search(r'<script id="model">(.*?)</script>', html, re.S)
    if not m:
        sys.exit("在 HTML 中找不到 <script id=\"model\">")

    rng = random.Random(20261119)
    cases = []

    # 固定用例
    fixed = [
        ([[-8192, -0.5, -0.25, -0.125]] + [[0] * 4] * 3,
         [[1024, 0, 0, 0]] + [[1, 0, 0, 0]] * 3,
         [[8388608, 0, 0, 0]] + [[0] * 4] * 3),
        ([[2.0 ** -24] * 4] * 4, [[1.0] * 4] * 4, [[1.0] * 4] * 4),
        ([[0.0] * 4] * 4, [[0.0] * 4] * 4, [[0.0] * 4] * 4),
    ]
    for A, B, C in fixed:
        c = make_case(A, B, C)
        if c:
            cases.append(c)

    while len(cases) < n:
        c = make_case(*gen_case(rng, len(cases) % 6))
        if c:
            cases.append(c)

    # 输入舍入：模拟器用 rneF16 / Math.fround，和 Python 的 struct 对拍
    rounding = []
    for _ in range(5000):
        k = rng.random()
        if k < 0.3:
            x = rng.gauss(0, 1)
        elif k < 0.6:
            x = log_uniform(rng, -30, 18)
        else:
            x = rng.uniform(-1, 1) * 10 ** rng.uniform(-8, 8)
        if not (abs(x) < 1e300):
            continue
        try:
            h = struct.unpack("<H", struct.pack("<e", x))[0]
        except OverflowError:
            h = 0x7C00 if x > 0 else 0xFC00
        rounding.append({"x": x, "h": h, "f": bits32(x)})

    with tempfile.TemporaryDirectory() as tmp:
        model = os.path.join(tmp, "model.js")
        data = os.path.join(tmp, "cases.json")
        rdata = os.path.join(tmp, "rounding.json")
        runner = os.path.join(tmp, "run.js")
        open(model, "w", encoding="utf-8").write(m.group(1))
        json.dump(cases, open(data, "w"))
        json.dump(rounding, open(rdata, "w"))
        open(runner, "w", encoding="utf-8").write(NODE_RUNNER)
        res = subprocess.run([node, runner, model, data, rdata], capture_output=True, text=True)
        print(res.stdout.strip())
        if res.returncode != 0:
            print(res.stderr.strip())
            sys.exit(1)


if __name__ == "__main__":
    main()
