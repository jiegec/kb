#!/usr/bin/env python3
"""抓取 consumer.huawei.com 的开源软件披露列表。

页面 https://consumer.huawei.com/en/opensource/detail/ 通过
`/cmkt/servlet/file/list` 接口拿数据，接口只校验 Referer，不需要登录。

每条记录对应一个「型号代码 + 系统版本」的开源包，例如：
    fileName: GRL-AL20_HarmonyOS6.1.0
    fileIntroduce: HUAWEI Mate XTs | ULTIMATE DESIGN,Greenlan,HarmonyOS6.1.0

用法：
    uv run python scripts/fetch_huawei_opensource.py
    uv run python scripts/fetch_huawei_opensource.py --out data/huawei_opensource.json
    uv run python scripts/fetch_huawei_opensource.py --model GRL-AL20   # 只看某个型号
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://consumer.huawei.com/cmkt/servlet/file/list"
REFERER = "https://consumer.huawei.com/en/opensource/detail/"
PAGE_SIZE = 100


def fetch_page(page: int, site_code: str = "worldwide") -> list[dict]:
    # 注意：GET 会忽略 curPage（永远返回第 1 页），必须用 POST 表单。
    body = urllib.parse.urlencode(
        {
            "siteCode": site_code,
            "fileType": "openSourceSoftware",
            "pageSize": PAGE_SIZE,
            "curPage": page,
        }
    ).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36",
            "Referer": REFERER,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8") or "[]")


def normalize(item: dict) -> dict:
    filename = item.get("fileName") or ""
    model, _, os_ver = filename.partition("_")
    intro = item.get("fileIntroduce") or ""
    parts = [p.strip() for p in intro.split(",")]
    product = parts[0] if parts else ""
    codename = parts[1] if len(parts) > 1 else ""
    return {
        "model": model,
        "product": product,
        "codename": codename,
        "os_version": item.get("fileVersion") or os_ver,
        "file_name": filename,
        "file_size": item.get("fileSize"),
        "release_date": item.get("releaseDate"),
        "download_url": item.get("downloadUrl"),
        "declare_url": item.get("declareDownloadUrl"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="data/huawei_opensource.json")
    ap.add_argument("--site-code", default="worldwide")
    ap.add_argument("--model", default=None, help="只保留某个型号代码，如 GRL-AL20")
    ap.add_argument("--max-pages", type=int, default=0)
    args = ap.parse_args()

    all_items: list[dict] = []
    seen: set = set()
    total = 0
    page = 1
    while True:
        try:
            items = fetch_page(page, args.site_code)
        except Exception as e:  # noqa: BLE001
            print(f"page {page} failed: {e}", file=sys.stderr)
            break
        if not items:
            break
        total = items[0].get("totalRows") or total
        added = 0
        for it in items:
            key = (it.get("fileInfoId"), it.get("fileName"), it.get("releaseDate"))
            if key in seen:
                continue
            seen.add(key)
            all_items.append(it)
            added += 1
        print(f"page {page}: +{added} new (total {len(all_items)}/{total})", file=sys.stderr)
        if added == 0:
            break
        if not total or len(all_items) >= total:
            break
        if args.max_pages and page >= args.max_pages:
            break
        page += 1
        time.sleep(0.3)

    entries = [normalize(x) for x in all_items]
    if args.model:
        entries = [e for e in entries if e["model"].upper() == args.model.upper()]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n")
    models = sorted({e["model"] for e in entries})
    print(f"写入 {out}：{len(entries)} 条，{len(models)} 个型号", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
