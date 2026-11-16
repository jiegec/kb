#!/usr/bin/env python3
"""抓取华为开发者文档「各版本支持设备型号清单」。

数据来自文档中心接口（SPA 使用的就是它）：
    POST https://svc-drcn.developer.huawei.com/community/servlet/consumer/cn/documentPortal/getCenterDocument
    {"centerPrefix":"doccenter","language":"cn","level2NodeAlias":"release-notes","isApi":0,"fileName":"support-device"}

返回的 content 是整篇 HTML，脚本按标题（版本 / 类别）切分并解析表格，
输出每个型号对应的型号代码。

用法：
    uv run python scripts/fetch_harmony_devices.py
    uv run python scripts/fetch_harmony_devices.py --out data/harmony_devices.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

API = "https://svc-drcn.developer.huawei.com/community/servlet/consumer/cn/documentPortal/getCenterDocument"
PAYLOAD = {
    "centerPrefix": "doccenter",
    "language": "cn",
    "level2NodeAlias": "release-notes",
    "isApi": 0,
    "fileName": "support-device",
}
CATEGORIES = {"Phone", "Tablet", "PC/2in1", "TV", "Wearable", "Lite Wearable"}
CODE_RE = re.compile(r"^[A-Z]{2,5}-[A-Z0-9]{1,6}$")


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[dict] = []
        self.version = ""
        self.category = ""
        self._table: dict | None = None
        self._row: list[dict] | None = None
        self._cell: dict | None = None
        self._in_h = False
        self._h_buf: list[str] = []

    # -- headings -------------------------------------------------
    def handle_starttag(self, tag, attrs):
        if tag == "h4":
            self._in_h = True
            self._h_buf = []
        elif tag == "table":
            self._table = {"version": self.version, "category": self.category, "rows": []}
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            a = dict(attrs)
            self._cell = {
                "text": [],
                "rowspan": int(a.get("rowspan") or 1),
                "colspan": int(a.get("colspan") or 1),
            }
        elif tag == "br" and self._cell is not None:
            self._cell["text"].append(" ")

    def handle_endtag(self, tag):
        if tag == "h4":
            self._in_h = False
            text = "".join(self._h_buf).strip()
            self._h_buf = []
            m = re.match(r"^\[h\d+\]\s*(.*)$", text)
            if m:
                self.category = m.group(1).strip()
            elif text:
                self.version = text
                self.category = ""
        elif tag in ("td", "th") and self._cell is not None and self._row is not None:
            self._cell["text"] = "".join(self._cell["text"])
            self._row.append(self._cell)
            self._cell = None
        elif tag == "tr" and self._row is not None and self._table is not None:
            if self._row:
                self._table["rows"].append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            self.tables.append(self._table)
            self._table = None

    def handle_data(self, data):
        if self._in_h:
            self._h_buf.append(data)
        if self._cell is not None:
            self._cell["text"].append(data)


def expand_grid(rows: list[list[dict]]) -> list[list[str]]:
    """按 rowspan/colspan 展开成规整网格。"""
    grid: list[list[str]] = []
    pending: dict[int, tuple[str, int]] = {}  # col -> (text, remaining rows)
    for row in rows:
        out: list[str] = []
        col = 0
        cells = list(row)
        while cells or any(c >= col for c in pending):
            if col in pending:
                text, left = pending[col]
                out.append(text)
                if left <= 1:
                    del pending[col]
                else:
                    pending[col] = (text, left - 1)
                col += 1
                continue
            if not cells:
                out.append("")
                col += 1
                continue
            cell = cells.pop(0)
            text = re.sub(r"\s+", " ", cell["text"]).strip()
            out.append(text)
            for _ in range(cell["colspan"]):
                if _ > 0:
                    out.append("")
            if cell["rowspan"] > 1:
                for k in range(cell["colspan"]):
                    pending[col + k] = (text, cell["rowspan"] - 1)
            col += cell["colspan"]
        grid.append(out)
    return grid


def split_codes(text: str) -> list[str]:
    parts = re.split(r"[\s,，、/]+", text.replace("\n", " ").strip())
    return [p for p in parts if CODE_RE.match(p)]


def parse_rows(rows: list[list[str]]) -> list[dict]:
    out: list[dict] = []
    series = ""
    for row in rows:
        cells = [c for c in row]
        if not any(cells) or cells[0] in ("设备系列", "设备型号"):
            continue
        if len(cells) >= 3:
            s, model, codes = cells[0], cells[1], cells[2]
            if s:
                series = s
        elif len(cells) == 2:
            model, codes = cells
        else:
            continue
        if not model or model in ("设备型号", "型号代码"):
            continue
        series = re.split(r"说明[：:]", series)[0].strip()
        out.append({"series": series, "model": model, "codes": split_codes(codes)})
    return out


def fetch() -> str:
    req = urllib.request.Request(
        API,
        data=json.dumps(PAYLOAD).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data["value"]["content"]["content"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="data/harmony_devices.json")
    args = ap.parse_args()

    parser = TableParser()
    parser.feed(fetch())

    entries: list[dict] = []
    seen = set()
    for t in parser.tables:
        cat = t["category"]
        if cat not in CATEGORIES:
            cat = next((c for c in CATEGORIES if c in cat), cat)
        for e in parse_rows(expand_grid(t["rows"])):
            e["version"] = t["version"]
            e["category"] = cat
            key = (e["version"], e["model"], tuple(e["codes"]))
            if key in seen:
                continue
            seen.add(key)
            entries.append(e)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n")
    versions = sorted({e["version"] for e in entries})
    print(f"写入 {out}：{len(entries)} 条，{len(versions)} 个版本", file=sys.stderr)
    for v in versions:
        n = sum(1 for e in entries if e["version"] == v)
        print(f"  {v}: {n}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
