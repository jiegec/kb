#!/usr/bin/env python3
"""抓取 consumer.huawei.com 的规格参数页，提取“处理器”信息。

consumer.huawei.com 的规格页是服务端渲染的静态 HTML，直接用 urllib 即可。

用法：
    uv run python scripts/fetch_consumer.py --category tablets
    uv run python scripts/fetch_consumer.py --category phones --out data/consumer_phones.json
    uv run python scripts/fetch_consumer.py --urls https://consumer.huawei.com/cn/tablets/matepad-pro-12/specs/
"""

from __future__ import annotations

import argparse
import html as htmllib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://consumer.huawei.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
CHIP_RE = re.compile(r"麒麟|Kirin|骁龙|Snapdragon|天玑|Dimensity|英特尔|AMD|Ultra|锐龙|酷睿")


def get(url: str, retries: int = 2) -> str:
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        except (urllib.error.URLError, TimeoutError):
            if i == retries:
                raise
            time.sleep(1.5)
    return ""


def text_lines(html: str) -> list[str]:
    txt = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S)
    txt = re.sub(r"<[^>]+>", "\n", txt)
    txt = htmllib.unescape(txt)
    return [l.strip() for l in txt.splitlines() if l.strip()]


def parse_specs(html: str) -> dict:
    title = ""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S)
    if m:
        title = htmllib.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    lines = text_lines(html)
    processor, note = "", ""
    for i, l in enumerate(lines):
        if l == "处理器":
            for j in range(i + 1, min(i + 4, len(lines))):
                if CHIP_RE.search(lines[j]):
                    processor = lines[j]
                    if j + 1 < len(lines) and lines[j + 1].startswith("*"):
                        note = lines[j + 1]
                    break
            break
    return {"title": title, "processor": processor, "note": note}


def discover(category: str) -> list[str]:
    """从 cn sitemap 里找出某个类目下所有 specs 页。"""
    xml = get(f"{BASE}/cn/sitemap.xml")
    prefix = f"{BASE}/cn/{category}/"
    urls = []
    for loc in re.findall(r"<loc>([^<]+)</loc>", xml):
        if loc.startswith(prefix) and loc.endswith("/specs/") and loc not in urls:
            urls.append(loc)
    return urls


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--category", default=None, help="phones / tablets / harmonyos-computer")
    ap.add_argument("--urls", nargs="*", default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default="data/consumer_specs.json")
    args = ap.parse_args()

    urls: list[str] = []
    if args.urls:
        urls = args.urls
    elif args.category:
        urls = discover(args.category)
    else:
        ap.error("需要 --category 或 --urls")

    if args.limit:
        urls = urls[: args.limit]

    out: list[dict] = []
    for i, url in enumerate(urls, 1):
        try:
            page = get(url)
        except Exception as e:  # noqa: BLE001
            print(f"[{i}/{len(urls)}] FAIL {url} {e}", file=sys.stderr)
            continue
        info = parse_specs(page)
        info["url"] = url
        out.append(info)
        print(f"[{i}/{len(urls)}] {info['title'][:40]} | {info['processor']}", file=sys.stderr, flush=True)
        time.sleep(0.7)

    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(f"写入 {path}（{len(out)} 个商品）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
