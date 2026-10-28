#!/usr/bin/env python3
"""抓取华为商城商品参数（型号 / CPU / 版本），输出结构化 JSON。

做法：启动一个带 remote debugging 的 Chrome，通过 CDP 打开商品页，
逐个点击"版本"选项，读取"已选"行与"CPU型号"字段，最后写入 JSON。
只依赖 Python 标准库（自己实现了一个最小的 WebSocket 客户端）。

用法：
    # 默认抓取 docs/hardware/huawei.md 产品型号表里出现的所有商品
    uv run python scripts/fetch_vmall.py

    # 抓指定商品
    uv run python scripts/fetch_vmall.py --ids 10086476013098 10086384396215

    # 从文件读（每行一个 prdId）
    uv run python scripts/fetch_vmall.py --ids-file ids.txt --out data/vmall.json

    # 看浏览器在干什么（非 headless）
    uv run python scripts/fetch_vmall.py --headful --ids 10086476013098

输出结构：
{
  "generated_at": "2026-10-28T20:00:00+08:00",
  "source": "https://www.vmall.com",
  "products": [
    {
      "product_id": "10086476013098",
      "url": "https://www.vmall.com/product/10086476013098.html",
      "name": "HUAWEI Mate 80 Pro",
      "variants": [
        {"label": "12GB+256GB", "selected": "曜石黑·12GB+256GB·麒麟9030",
         "color": "曜石黑", "capacity": "12GB+256GB", "cpu": "麒麟9030",
         "models": ["SGT-AL50"]}
      ]
    }
  ]
}
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
    "chromium-browser",
]

DEFAULT_OUT = "data/vmall_products.json"
DOC = "docs/hardware/huawei.md"

# 页面上型号代码的形态：SGT-AL50 / GEM-W00 / VDE-AL10 / HED-AL00
MODEL_RE = re.compile(r"[A-Z]{2,3}-(?:AL|AN|W)\d{2}[a-z]?")
# 版本选项：12GB+256GB / 256GB / WiFi 12GB+512GB / 悦享款 12GB+256GB
VERSION_RE = re.compile(r"(\d+\s*GB(\s*\+\s*\d+\s*(?:GB|TB))?|WiFi|全网通|柔光|典藏)")


def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def find_chrome(explicit: str | None) -> str:
    if explicit:
        return explicit
    for c in CHROME_CANDIDATES:
        if os.path.sep in c:
            if Path(c).exists():
                return c
        else:
            from shutil import which

            w = which(c)
            if w:
                return w
    raise SystemExit("找不到 Chrome，用 --chrome 指定路径")


class WS:
    """最小 WebSocket 客户端，够跑 CDP。"""

    def __init__(self, url: str):
        u = urllib.parse.urlparse(url)
        self.host, self.port = u.hostname, u.port or 80
        path = u.path + (("?" + u.query) if u.query else "")
        self.sock = socket.create_connection((self.host, self.port), timeout=30)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)
        if b"101" not in resp.split(b"\r\n", 1)[0]:
            raise RuntimeError(f"WebSocket 握手失败: {resp[:100]!r}")
        self.buf = b""

    def _recv_exact(self, n: int) -> bytes:
        while len(self.buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise ConnectionError("socket closed")
            self.buf += chunk
        data, self.buf = self.buf[:n], self.buf[n:]
        return data

    def _recv_frame(self) -> tuple[bool, int, bytes]:
        b1, b2 = self._recv_exact(2)
        fin = bool(b1 & 0x80)
        opcode = b1 & 0x0F
        masked = b2 & 0x80
        length = b2 & 0x7F
        if length == 126:
            (length,) = struct.unpack(">H", self._recv_exact(2))
        elif length == 127:
            (length,) = struct.unpack(">Q", self._recv_exact(8))
        mask = self._recv_exact(4) if masked else b""
        payload = self._recv_exact(length)
        if masked:
            payload = bytes(c ^ mask[i % 4] for i, c in enumerate(payload))
        return fin, opcode, payload

    def recv_text(self) -> str:
        chunks = []
        while True:
            fin, opcode, payload = self._recv_frame()
            if opcode == 0x8:
                raise ConnectionError("closed")
            if opcode == 0x9:  # ping
                self._send_frame(0xA, payload)
                continue
            chunks.append(payload)
            if fin:
                return b"".join(chunks).decode()

    def _send_frame(self, opcode: int, data: bytes):
        header = bytes([0x80 | opcode])
        n = len(data)
        if n < 126:
            header += bytes([0x80 | n])
        elif n < 65536:
            header += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            header += bytes([0x80 | 127]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        masked = bytes(c ^ mask[i % 4] for i, c in enumerate(data))
        self.sock.sendall(header + mask + masked)

    def send(self, obj: dict):
        self._send_frame(0x1, json.dumps(obj).encode())

    def close(self):
        try:
            self._send_frame(0x8, b"")
        except Exception:
            pass
        self.sock.close()


class CDP:
    def __init__(self, ws_url: str):
        self.ws = WS(ws_url)
        self.next_id = 0

    def call(self, method: str, params: dict | None = None, timeout: float = 60):
        self.next_id += 1
        mid = self.next_id
        self.ws.send({"id": mid, "method": method, "params": params or {}})
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = json.loads(self.ws.recv_text())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"CDP {method} 失败: {msg['error']}")
                return msg.get("result", {})
        raise TimeoutError(method)

    def eval(self, expr: str, timeout: float = 60):
        r = self.call(
            "Runtime.evaluate",
            {"expression": expr, "returnByValue": True, "awaitPromise": True},
            timeout=timeout,
        )
        return r.get("result", {}).get("value")

    def close(self):
        self.ws.close()


def http_json(url: str, method: str = "GET"):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read().decode()
    return json.loads(body) if body.strip().startswith(("{", "[")) else body


def wait_for_chrome(port: int, timeout: float = 30) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            http_json(f"http://127.0.0.1:{port}/json/version")
            return
        except Exception:
            time.sleep(0.3)
    raise SystemExit(f"Chrome 在 {port} 端口没有起来")


EXTRACT_JS = r"""
(async () => {
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const readSelected = () => {
    const t = document.body.innerText;
    const sel = (t.match(/已选：([^\n]+)/) || [])[1] || "";
    const cpu = (t.match(/CPU型号\s*\n\s*([^\n]+)/) || [])[1] || "";
    const models = [...new Set(t.match(/[A-Z]{2,3}-(?:AL|AN|W)\d{2}[a-z]?/g) || [])];
    return { selected: sel.trim(), cpu: cpu.trim(), models };
  };
  const parse = (s) => {
    const parts = s.split("·").map((x) => x.trim()).filter(Boolean);
    return { color: parts[0] || "", capacity: parts[1] || "", cpu: parts[2] || "" };
  };
  const visible = (el) => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  const isVersion = (el) =>
    el.children.length === 0 &&
    el.innerText &&
    visible(el) &&
    el.innerText.trim().length < 26 &&
    /(\d+GB(\+\d+(GB|TB))?|WiFi|全网通|柔光|典藏)/.test(el.innerText) &&
    !/HUAWEI|华为|¥|评价|已选/.test(el.innerText);

  const versions = [];
  const seen = new Set();
  for (const el of document.querySelectorAll("div,span,li,button")) {
    if (!isVersion(el)) continue;
    const label = el.innerText.trim();
    if (seen.has(label)) continue;
    seen.add(label);
    versions.push({ el, label });
  }

  const out = [];
  const push = (label) => {
    const r = readSelected();
    const p = parse(r.selected);
    out.push({
      label,
      selected: r.selected,
      color: p.color,
      capacity: p.capacity,
      cpu: r.cpu || p.cpu,
      models: r.models,
    });
  };

  push("默认");
  for (const v of versions.slice(0, 10)) {
    v.el.click();
    await sleep(450);
    push(v.label);
  }
  return out;
})()
"""


def title_from_page(txt: str) -> str:
    for line in txt.splitlines():
        if line.startswith("首页") and ">" in line:
            return line.split(">", 1)[1].strip()
    return txt.splitlines()[0].strip() if txt else ""


def scrape_product(cdp: CDP, pid: str, wait: float) -> dict:
    url = f"https://www.vmall.com/product/{pid}.html"
    cdp.call("Page.navigate", {"url": url})
    time.sleep(wait)

    # 等页面出现"已选"或"CPU型号"
    deadline = time.time() + 25
    while time.time() < deadline:
        txt = cdp.eval("document.body.innerText", timeout=30) or ""
        if "已选" in txt or "CPU型号" in txt:
            break
        time.sleep(1)

    variants = cdp.eval(EXTRACT_JS, timeout=120) or []
    txt = cdp.eval("document.body.innerText", timeout=30) or ""
    full = title_from_page(txt)
    # "HUAWEI Mate 80 Pro 16GB+1TB 雪域白" -> "HUAWEI Mate 80 Pro"
    name = re.split(r"\s+\d+\s*GB", full, maxsplit=1)[0].strip() or full
    m = re.search(r"上市时间\s*\n\s*([^\n]+)", txt)
    launch_date = m.group(1).strip() if m else ""
    ym = re.search(r"(\d{4})\s*年\s*(\d{1,2})\s*月", launch_date)
    launch_year = int(ym.group(1)) if ym else None
    launch_month = int(ym.group(2)) if ym else None
    seen, uniq = set(), []
    for v in variants:
        key = v.get("selected") or v.get("label")
        if key in seen:
            continue
        seen.add(key)
        uniq.append(v)
    return {
        "product_id": pid,
        "url": url,
        "name": name,
        "title": full,
        "launch_date": launch_date,
        "launch_year": launch_year,
        "launch_month": launch_month,
        "variants": uniq,
    }


def ids_from_doc(path: Path) -> list[str]:
    text = path.read_text()
    return sorted(set(re.findall(r"vmall\.com/product/(\d+)\.html", text)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ids", nargs="*", default=None, help="商品 prdId，留空则从文档表格提取")
    ap.add_argument("--ids-file", help="每行一个 prdId")
    ap.add_argument("--doc", default=DOC, help=f"从该文件的表格提取 prdId（默认 {DOC}）")
    ap.add_argument("--out", default=DEFAULT_OUT, help=f"输出 JSON（默认 {DEFAULT_OUT}）")
    ap.add_argument("--chrome", default=None, help="Chrome 可执行文件路径")
    ap.add_argument("--port", type=int, default=9333)
    ap.add_argument("--wait", type=float, default=5.0, help="打开页面后等待秒数")
    ap.add_argument("--headful", action="store_true", help="有界面运行（默认 headless）")
    args = ap.parse_args()

    if args.ids:
        ids = args.ids
    elif args.ids_file:
        ids = [l.strip() for l in Path(args.ids_file).read_text().splitlines() if l.strip()]
    else:
        ids = ids_from_doc(Path(args.doc))
    ids = [i for i in dict.fromkeys(ids) if i]
    if not ids:
        print("没有商品 id", file=sys.stderr)
        return 1

    # 端口上已经有 Chrome 就直接复用，否则自己拉一个
    reuse = False
    try:
        http_json(f"http://127.0.0.1:{args.port}/json/version")
        reuse = True
        print(f"复用 127.0.0.1:{args.port} 上的 Chrome", file=sys.stderr)
    except Exception:
        pass

    chrome = find_chrome(args.chrome) if not reuse else None
    profile = None
    cmd = [
        chrome,
        "--remote-debugging-port=%d" % args.port,
        "--user-data-dir={profile}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-crash-reporter",
        "--disable-breakpad",
        "--disable-gpu",
        "--no-sandbox",
    ]
    if not args.headful:
        cmd.append("--headless=new")
    cmd.append("about:blank")
    proc = None
    if not reuse:
        profile = tempfile.mkdtemp(prefix="vmall-chrome-")
        cmd = [c.replace("{profile}", profile) for c in cmd]
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    products = []
    try:
        wait_for_chrome(args.port)
        tab = http_json(f"http://127.0.0.1:{args.port}/json/new?about:blank", method="PUT")
        cdp = CDP(tab["webSocketDebuggerUrl"])
        cdp.call("Page.enable")
        for n, pid in enumerate(ids, 1):
            print(f"[{n}/{len(ids)}] {pid}", file=sys.stderr, flush=True)
            try:
                products.append(scrape_product(cdp, pid, args.wait))
            except Exception as e:
                print(f"  失败: {e}", file=sys.stderr)
                products.append({"product_id": pid, "url": f"https://www.vmall.com/product/{pid}.html", "error": str(e)})
        cdp.close()
    finally:
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
        if profile:
            shutil.rmtree(profile, ignore_errors=True)

    out = {
        "generated_at": now_iso(),
        "source": "https://www.vmall.com",
        "products": products,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"写入 {out_path}（{len(products)} 个商品）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
