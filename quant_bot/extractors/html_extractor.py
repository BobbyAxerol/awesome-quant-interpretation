# -*- coding: utf-8 -*-
"""
quant_bot.extractors.html_extractor — QuantStats HTML extractor class.
"""

import re
from typing import Dict, List, Any
from bs4 import BeautifulSoup
from .base import BaseExtractor

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


def normalize_key(raw: str) -> str:
    s = raw.strip().lower()
    s = s.replace("﹪", "pct").replace("%", "pct")
    s = s.replace("√2", "sqrt2").replace("(ann.)", "ann")
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", "_", s.strip())
    return s


class QuantStatsHTMLExtractor(BaseExtractor):
    """Extractor for parsing QuantStats HTML reports."""

    def __init__(self, html_path: str):
        self.html_path = html_path
        self._soup: BeautifulSoup = None

    def _load_soup(self) -> BeautifulSoup:
        if self._soup is None:
            with open(self.html_path, encoding="utf-8") as f:
                self._soup = BeautifulSoup(f.read(), "lxml")
        return self._soup

    def extract_svgs(self) -> Dict[str, str]:
        soup = self._load_soup()
        svgs = soup.find_all("svg")
        if len(svgs) != len(SLOT_ORDER):
            print(f"[CẢNH BÁO] Tìm thấy {len(svgs)} SVG, kỳ vọng {len(SLOT_ORDER)}.")
        out = {}
        for i, slot in enumerate(SLOT_ORDER):
            if i < len(svgs):
                svg_str = str(svgs[i])
                svg_str = re.sub(r"<svg ", '<svg class="qs-chart" ', svg_str, count=1)
                out[slot] = svg_str
        return out

    def extract_kpi(self) -> Dict[str, str]:
        soup = self._load_soup()
        h3 = soup.find(lambda t: t.name == "h3" and "Key Performance Metrics" in t.get_text())
        if not h3:
            return {}
        table = h3.find_next("table")
        rows = self._table_to_rows(table)[1:]
        kpi = {}
        for r in rows:
            if len(r) == 2 and r[0]:
                kpi[normalize_key(r[0])] = r[1]
        return kpi

    def extract_eoy(self) -> List[Dict[str, str]]:
        soup = self._load_soup()
        h3 = soup.find(lambda t: t.name == "h3" and "EOY Returns" in t.get_text())
        if not h3:
            return []
        table = h3.find_next("table")
        rows = self._table_to_rows(table)[1:]
        return [{"year": r[0], "return": r[1], "cumulative": r[2]} for r in rows if len(r) >= 3]

    def extract_drawdowns(self) -> List[Dict[str, str]]:
        soup = self._load_soup()
        h3 = soup.find(lambda t: t.name == "h3" and "Drawdowns" in t.get_text())
        if not h3:
            return []
        table = h3.find_next("table")
        rows = self._table_to_rows(table)[1:]
        return [{"started": r[0], "recovered": r[1], "drawdown": r[2], "days": r[3]}
                for r in rows if len(r) >= 4]

    def extract_meta(self) -> Dict[str, Any]:
        soup = self._load_soup()
        h1 = soup.find("h1")
        h4 = soup.find("h4")
        title = h1.get_text(" ", strip=True) if h1 else ""
        subtitle = h4.get_text(" ", strip=True) if h4 else ""
        m = re.search(r"(\d{1,2}\s+\w+,?\s+\d{4})\s*-\s*(\d{1,2}\s+\w+,?\s+\d{4})", title)
        date_start, date_end = (m.group(1), m.group(2)) if m else (None, None)
        return {"title": title, "subtitle": subtitle, "date_start": date_start, "date_end": date_end}

    def _table_to_rows(self, table) -> List[List[str]]:
        rows = []
        for tr in table.find_all("tr"):
            cells = [c.get_text(strip=True) for c in tr.find_all(["td", "th"])]
            if any(cells):
                rows.append(cells)
        return rows

    def extract(self) -> Dict[str, Any]:
        return {
            "meta": self.extract_meta(),
            "svgs": self.extract_svgs(),
            "kpi": self.extract_kpi(),
            "eoy": self.extract_eoy(),
            "drawdowns": self.extract_drawdowns(),
        }
