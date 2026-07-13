# -*- coding: utf-8 -*-
"""
qs_extract.py — Trích xuất dữ liệu từ file HTML do quantstats.reports.html() xuất ra.

Giả định cố định (khớp với cách quantstats sinh report không kèm benchmark, mode="full"):
- Đúng 12 SVG chart, theo ĐÚNG thứ tự cố định bên dưới.
- Nếu bạn đổi cách gọi quantstats (thêm benchmark, đổi mode...) số lượng/thứ tự chart
  có thể khác đi -> cần calibrate lại SLOT_ORDER.
"""
from bs4 import BeautifulSoup
import re

SLOT_ORDER = [
    "cumulative_return",        # 0
    "cumulative_return_log",    # 1
    "eoy_returns_chart",        # 2
    "monthly_dist",             # 3
    "daily_returns",            # 4
    "rolling_vol",              # 5
    "rolling_sharpe",           # 6
    "rolling_sortino",          # 7
    "worst_dd_periods",         # 8
    "underwater",               # 9
    "monthly_heatmap",          # 10
    "return_quantiles",         # 11
]

def _normalize_key(raw: str) -> str:
    s = raw.strip().lower()
    s = s.replace("﹪", "pct").replace("%", "pct")
    s = s.replace("√2", "sqrt2").replace("(ann.)", "ann")
    s = re.sub(r"[^\w\s]", "", s)      # bỏ dấu câu còn lại
    s = re.sub(r"\s+", "_", s.strip())
    return s

def load_soup(html_path: str) -> BeautifulSoup:
    with open(html_path, encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "lxml")

def extract_svgs(soup: BeautifulSoup) -> dict:
    svgs = soup.find_all("svg")
    if len(svgs) != len(SLOT_ORDER):
        print(f"[CẢNH BÁO] Tìm thấy {len(svgs)} SVG, kỳ vọng {len(SLOT_ORDER)}. "
              f"Thứ tự slot có thể không còn đúng — hãy chạy sanity_check() trước khi tin kết quả.")
    out = {}
    for i, slot in enumerate(SLOT_ORDER):
        if i < len(svgs):
            svg_str = str(svgs[i])
            svg_str = re.sub(r"<svg ", '<svg class="qs-chart" ', svg_str, count=1)
            out[slot] = svg_str
    return out

def _table_to_rows(table) -> list:
    rows = []
    for tr in table.find_all("tr"):
        cells = [c.get_text(strip=True) for c in tr.find_all(["td", "th"])]
        if any(cells):
            rows.append(cells)
    return rows

def extract_kpi(soup: BeautifulSoup) -> dict:
    h3 = soup.find(lambda t: t.name == "h3" and "Key Performance Metrics" in t.get_text())
    table = h3.find_next("table")
    rows = _table_to_rows(table)[1:]  # bỏ header
    kpi = {}
    for r in rows:
        if len(r) == 2 and r[0]:
            kpi[_normalize_key(r[0])] = r[1]
    return kpi

def extract_eoy(soup: BeautifulSoup) -> list:
    h3 = soup.find(lambda t: t.name == "h3" and "EOY Returns" in t.get_text())
    table = h3.find_next("table")
    rows = _table_to_rows(table)[1:]
    return [{"year": r[0], "return": r[1], "cumulative": r[2]} for r in rows if len(r) >= 3]

def extract_drawdowns(soup: BeautifulSoup) -> list:
    h3 = soup.find(lambda t: t.name == "h3" and "Drawdowns" in t.get_text())
    table = h3.find_next("table")
    rows = _table_to_rows(table)[1:]
    return [{"started": r[0], "recovered": r[1], "drawdown": r[2], "days": r[3]}
            for r in rows if len(r) >= 4]

def extract_meta(soup: BeautifulSoup) -> dict:
    h1 = soup.find("h1")
    h4 = soup.find("h4")
    title = h1.get_text(" ", strip=True) if h1 else ""
    subtitle = h4.get_text(" ", strip=True) if h4 else ""
    # title thường dạng: "... 2 Jan, 2020 - 10 Jul, 2026"
    m = re.search(r"(\d{1,2}\s+\w+,?\s+\d{4})\s*-\s*(\d{1,2}\s+\w+,?\s+\d{4})", title)
    date_start, date_end = (m.group(1), m.group(2)) if m else (None, None)
    return {"title": title, "subtitle": subtitle, "date_start": date_start, "date_end": date_end}

def extract_all(html_path: str) -> dict:
    soup = load_soup(html_path)
    return {
        "meta": extract_meta(soup),
        "svgs": extract_svgs(soup),
        "kpi": extract_kpi(soup),
        "eoy": extract_eoy(soup),
        "drawdowns": extract_drawdowns(soup),
    }

if __name__ == "__main__":
    import sys, json
    data = extract_all(sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/quantstats_daily.html")
    print(f"SVG slots: {list(data['svgs'].keys())}")
    print(f"KPI keys ({len(data['kpi'])}): {list(data['kpi'].keys())[:10]} ...")
    print(f"EOY rows: {len(data['eoy'])}")
    print(f"Drawdown rows: {len(data['drawdowns'])}")