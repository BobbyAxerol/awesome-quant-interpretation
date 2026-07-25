# -*- coding: utf-8 -*-
"""
quant_bot.analyzers.stress_monthly — Stress Test Analysis and Monthly Returns Heatmap Builder.
Calculates crisis period resilience and monthly return heatmaps matching paper theme aesthetics.
"""

from collections import defaultdict
from typing import List, Dict, Any, Optional
from ..domain.trade import EquityPoint


class StressTestAnalyzer:
    """Calculates strategy resilience vs benchmark during historical stress periods."""

    DEFAULT_PERIODS = [
        {"name": "COVID-19 Crash", "start": "2020-02-19", "end": "2020-03-23", "benchmark": "-28.7%"},
        {"name": "2021 Crypto Mining Ban", "start": "2021-05-10", "end": "2021-07-20", "benchmark": "-51.4%"},
        {"name": "2022 Bear Market", "start": "2022-01-03", "end": "2022-10-12", "benchmark": "-67.3%"},
        {"name": "2022 LUNA & FTX Crash", "start": "2022-05-05", "end": "2022-11-20", "benchmark": "-58.2%"},
        {"name": "2024 Market Shakeout", "start": "2024-03-15", "end": "2024-08-05", "benchmark": "-22.5%"},
    ]

    def __init__(self, equity_curve: List[EquityPoint], periods: Optional[List[Dict[str, str]]] = None):
        self.equity_curve = equity_curve
        self.periods = periods or self.DEFAULT_PERIODS

    def analyze(self) -> List[Dict[str, Any]]:
        if not self.equity_curve:
            return []

        results = []
        for p in self.periods:
            pts = [pt for pt in self.equity_curve if p["start"] <= pt.timestamp[:10] <= p["end"]]
            if pts:
                start_eq = pts[0].equity
                end_eq = pts[-1].equity
                pnl_pct = ((end_eq / start_eq) - 1.0) * 100.0 if start_eq > 0 else 0.0
                results.append({
                    "name": p["name"],
                    "dates": f"{p['start']} → {p['end']}",
                    "portfolio_pnl": pnl_pct,
                    "benchmark": p["benchmark"]
                })
        return results

    def render_html_table(self) -> str:
        data = self.analyze()
        if not data:
            return ""

        rows = []
        for r in data:
            pnl_val = r["portfolio_pnl"]
            pnl_class = "color: #10B981; font-weight: 600;" if pnl_val >= 0 else "color: #EF4444; font-weight: 600;"
            rows.append(f"""
          <tr>
            <td style="padding: 10px 14px; font-weight: 600; color: #181B20;">{r['name']}</td>
            <td style="padding: 10px 14px; font-family: var(--font-mono); color: #565C63; font-size: 12px;">{r['dates']}</td>
            <td style="padding: 10px 14px; text-align: right; font-family: var(--font-mono); {pnl_class}">{pnl_val:+.1f}%</td>
            <td style="padding: 10px 14px; text-align: right; font-family: var(--font-mono); color: #565C63;">{r['benchmark']}</td>
          </tr>
""")

        html = f"""
<div class="stress-test-card" style="border: 1px solid var(--line); border-radius: 6px; background: #FFFFFF; margin: 24px 0; overflow: hidden; box-shadow: var(--shadow);">
  <div style="padding: 14px 18px; border-bottom: 1px solid var(--line-soft); background: var(--paper-raised);">
    <h3 style="margin: 0; font-family: var(--font-display); font-size: 15px; color: var(--ink);">Stress Test Analysis</h3>
  </div>
  <table width="100%" style="border-collapse: collapse; font-size: 13px;">
    <thead>
      <tr style="border-bottom: 1px solid var(--line); color: var(--ink-soft); font-family: var(--font-mono); font-size: 11px; text-transform: uppercase;">
        <th style="padding: 10px 14px; text-align: left;">Crisis Period</th>
        <th style="padding: 10px 14px; text-align: left;">Dates</th>
        <th style="padding: 10px 14px; text-align: right;">Portfolio</th>
        <th style="padding: 10px 14px; text-align: right;">Benchmark (Asset)</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</div>
""".strip()
        return html


class MonthlyReturnsHeatmapBuilder:
    """Builds a styled Monthly Returns Heatmap table matching paper theme aesthetics."""

    MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def __init__(self, equity_curve: List[EquityPoint]):
        self.equity_curve = equity_curve

    def analyze(self) -> Dict[int, Dict[str, Any]]:
        if not self.equity_curve:
            return {}

        by_year = defaultdict(list)
        for pt in self.equity_curve:
            yr = int(pt.timestamp[:4])
            by_year[yr].append(pt)

        matrix = {}
        for yr in sorted(by_year.keys()):
            pts_yr = by_year[yr]
            yr_start_eq = pts_yr[0].equity
            yr_end_eq = pts_yr[-1].equity
            total_ret = ((yr_end_eq / yr_start_eq) - 1.0) * 100.0 if yr_start_eq > 0 else 0.0

            max_dd = max([abs(pt.drawdown) * 100.0 if abs(pt.drawdown) <= 1.0 else abs(pt.drawdown) for pt in pts_yr])

            by_m = defaultdict(list)
            for pt in pts_yr:
                m = int(pt.timestamp[5:7])
                by_m[m].append(pt)

            monthly = {}
            for m in range(1, 13):
                if m in by_m:
                    m_pts = by_m[m]
                    m_ret = ((m_pts[-1].equity / m_pts[0].equity) - 1.0) * 100.0 if m_pts[0].equity > 0 else 0.0
                    monthly[m] = round(m_ret, 1)
                else:
                    monthly[m] = None

            matrix[yr] = {
                "monthly": monthly,
                "total": round(total_ret, 1),
                "max_dd": round(max_dd, 1)
            }
        return matrix

    def render_html_table(self) -> str:
        matrix = self.analyze()
        if not matrix:
            return ""

        header_cols = "".join(f'<th style="padding: 8px 6px; text-align: center;">{m}</th>' for m in self.MONTH_NAMES)
        rows = []

        for yr in sorted(matrix.keys()):
            yr_data = matrix[yr]
            m_cells = []

            for m in range(1, 13):
                val = yr_data["monthly"].get(m)
                if val is None:
                    m_cells.append('<td style="padding: 8px 6px; text-align: center; color: #A3A8AF; font-size: 11px;">—</td>')
                else:
                    # Cell background styling based on value
                    if val > 0:
                        alpha = min(0.65, max(0.12, val / 25.0))
                        bg = f"background: rgba(16, 185, 129, {alpha:.2f}); color: #065F46; font-weight: 600;"
                    elif val < 0:
                        alpha = min(0.65, max(0.12, abs(val) / 15.0))
                        bg = f"background: rgba(239, 68, 68, {alpha:.2f}); color: #991B1B; font-weight: 600;"
                    else:
                        bg = "background: #F3F4F6; color: #565C63;"

                    m_cells.append(f'<td style="padding: 8px 4px; text-align: center; font-family: var(--font-mono); font-size: 11.5px; border: 1px solid #FFFFFF; {bg}">{val:+.1f}</td>')

            tot_val = yr_data["total"]
            tot_style = "color: #10B981; font-weight: 700;" if tot_val >= 0 else "color: #EF4444; font-weight: 700;"
            mdd_val = yr_data["max_dd"]

            rows.append(f"""
          <tr style="border-bottom: 1px solid var(--line-soft);">
            <td style="padding: 8px 10px; font-weight: 700; font-family: var(--font-mono); color: #181B20;">{yr}</td>
            {''.join(m_cells)}
            <td style="padding: 8px 8px; text-align: right; font-family: var(--font-mono); font-size: 12px; {tot_style}">{tot_val:+.1f}%</td>
            <td style="padding: 8px 8px; text-align: right; font-family: var(--font-mono); font-size: 12px; color: #AC3B34;">-{mdd_val:.1f}%</td>
          </tr>
""")

        html = f"""
<div class="monthly-returns-card" style="border: 1px solid var(--line); border-radius: 6px; background: #FFFFFF; margin: 24px 0; overflow: hidden; box-shadow: var(--shadow);">
  <div style="padding: 14px 18px; border-bottom: 1px solid var(--line-soft); background: var(--paper-raised);">
    <h3 style="margin: 0; font-family: var(--font-display); font-size: 15px; color: var(--ink);">Monthly Returns (%) &amp; Annual Max Drawdown</h3>
  </div>
  <div style="overflow-x: auto;">
    <table width="100%" style="border-collapse: collapse; font-size: 12.5px;">
      <thead>
        <tr style="border-bottom: 1px solid var(--line); color: var(--ink-soft); font-family: var(--font-mono); font-size: 11px; text-transform: uppercase; background: var(--paper-raised);">
          <th style="padding: 8px 10px; text-align: left;">Year</th>
          {header_cols}
          <th style="padding: 8px 8px; text-align: right;">Total</th>
          <th style="padding: 8px 8px; text-align: right;">MaxDD</th>
        </tr>
      </thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
  </div>
</div>
""".strip()
        return html
