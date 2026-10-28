#!/usr/bin/env python3
"""在华为商城按关键词搜索，自动发现商品 prdId。

思路：打开搜索页，滚动加载，然后逐个点击商品卡片——卡片点击会新开一个
tab，URL 里带 prdId；记录后关掉 tab。发现到的 id 可以交给
`fetch_vmall.py --ids-file` 去抓型号和参数。

用法：
    # 默认搜三类：手机 / 平板 / 笔记本
    uv run python scripts/discover_vmall.py

    # 指定关键词，每个关键词最多点 10 个卡片
    uv run python scripts/discover_vmall.py --keywords MatePad MateBook --max-products 10

    # 只输出 id（默认也输出 name）
    uv run python scripts/discover_vmall.py --out data/vmall_ids.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_vmall as fv


def open_tab(port: int, url: str = "about:blank") -> dict:
    return fv.http_json(f"http://127.0.0.1:{port}/json/new?" + urllib.parse.quote(url, safe=""), method="PUT")


def close_tab(port: int, tab_id: str) -> None:
    try:
        fv.http_json(f"http://127.0.0.1:{port}/json/close/{tab_id}")
    except Exception:
        pass


def discover(keyword: str, port: int, max_scroll: int, max_products: int) -> list[dict]:
    url = ("https://www.vmall.com/portal/search/index.html?targetRoute=searchresult&searchWord="
           + urllib.parse.quote(keyword, safe=""))
    tab = open_tab(port, url)
    cdp = fv.CDP(tab["webSocketDebuggerUrl"])
    cdp.call("Page.enable")
    time.sleep(6)

    found: dict[str, str] = {}
    done = set()
    for _ in range(max_scroll + 1):
        cdp.eval("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2.0)

        total = cdp.eval("document.querySelectorAll('[data-testid$=\"-searchProduct\"]').length") or 0
        for idx in range(int(total)):
            if len(found) >= max_products:
                break
            if idx in done:
                continue
            done.add(idx)

            box = cdp.eval(
                "(()=>{const e=document.querySelector('[data-testid=\"%d-searchProduct\"]');"
                "if(!e)return '';e.scrollIntoView({block:'center'});"
                "const r=e.getBoundingClientRect();"
                "return JSON.stringify({x:r.x+r.width/2,y:r.y+r.height/2,"
                "lines:e.innerText.split('\\n').slice(0,5)});})()" % idx
            )
            try:
                info = json.loads(box)
                x, y = info["x"], info["y"]
            except (json.JSONDecodeError, TypeError, ValueError):
                continue
            name = ""
            for line in info.get("lines", []):
                line = line.strip()
                if line and line not in ("新品", "赠品") and len(line) > 2:
                    name = line
                    break

            before = {p["id"] for p in fv.http_json(f"http://127.0.0.1:{port}/json/list") if p["type"] == "page"}
            cdp.call("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1})
            cdp.call("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1})

            pid = ""
            for _ in range(10):
                time.sleep(0.5)
                for pg in fv.http_json(f"http://127.0.0.1:{port}/json/list"):
                    if pg["type"] != "page" or pg["id"] in before:
                        continue
                    if "prdId=" in pg["url"]:
                        pid = pg["url"].split("prdId=")[-1].split("&")[0]
                        close_tab(port, pg["id"])
                        break
                if pid:
                    break
            if pid and pid not in found:
                found[pid] = name

    cdp.close()
    close_tab(port, tab["id"])
    return [{"product_id": k, "name": v} for k, v in found.items()]

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keywords", nargs="*", default=["手机", "平板", "笔记本"])
    ap.add_argument("--max-scroll", type=int, default=1, help="每个关键词额外滚动几次（每次约 20 个商品）")
    ap.add_argument("--max-products", type=int, default=20, help="每个关键词最多点开多少个商品")
    ap.add_argument("--port", type=int, default=9333)
    ap.add_argument("--out", default="data/vmall_ids.json")
    ap.add_argument("--chrome", default=None)
    args = ap.parse_args()

    chrome = fv.find_chrome(args.chrome)
    profile = tempfile.mkdtemp(prefix="vmall-discover-")
    proc = subprocess.Popen(
        [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--remote-debugging-port=%d" % args.port,
         "--user-data-dir=" + profile, "--no-first-run", "--no-default-browser-check", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    result = {}
    try:
        fv.wait_for_chrome(args.port)
        for kw in args.keywords:
            print(f"[discover] {kw}", file=sys.stderr, flush=True)
            result[kw] = discover(kw, args.port, args.max_scroll, args.max_products)
            print(f"  -> {len(result[kw])} 个", file=sys.stderr, flush=True)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        import shutil

        shutil.rmtree(profile, ignore_errors=True)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"写入 {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
