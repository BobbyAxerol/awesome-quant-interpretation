# -*- coding: utf-8 -*-
"""
quant_bot.charts.trade_overlay — SVG chart generator for trade entry/exit overlay on equity/price curves.
"""

from typing import List, Optional
from ..domain.trade import Trade, EquityPoint
from .base import BaseChartGenerator


class EquityTradeOverlayChart(BaseChartGenerator):
    """Generates an SVG chart overlaying trade entry/exit signals onto the Equity Curve."""

    def __init__(self, equity_curve: List[EquityPoint], trades: List[Trade], width: int = 800, height: int = 350):
        self.equity_curve = equity_curve
        self.trades = trades
        self.width = width
        self.height = height

    def render_svg(self) -> str:
        if not self.equity_curve:
            return '<div class="chart-error">Không đủ dữ liệu Equity Curve</div>'

        padding = 50
        w = self.width - 2 * padding
        h = self.height - 2 * padding

        equities = [pt.equity for pt in self.equity_curve]
        min_eq = min(equities)
        max_eq = max(equities)
        if max_eq == min_eq:
            max_eq += 1.0

        n_pts = len(self.equity_curve)

        def get_coords(idx: int, eq_val: float):
            x = padding + (idx / max(1, n_pts - 1)) * w
            y = padding + h - ((eq_val - min_eq) / (max_eq - min_eq)) * h
            return x, y

        # Build equity polyline path
        path_pts = []
        for i, pt in enumerate(self.equity_curve):
            x, y = get_coords(i, pt.equity)
            path_pts.append(f"{x:.1f},{y:.1f}")
        path_str = " ".join(path_pts)

        # Map timestamps to equity curve indices for trade overlay
        ts_index_map = {pt.timestamp: i for i, pt in enumerate(self.equity_curve)}

        trade_markers = []
        for t in self.trades[:100]:  # render top 100 trades to keep SVG light
            open_idx = ts_index_map.get(t.open_datetime)
            close_idx = ts_index_map.get(t.close_datetime)

            if open_idx is not None:
                ox, oy = get_coords(open_idx, self.equity_curve[open_idx].equity)
                color = "#10B981" if t.is_long else "#EF4444"
                symbol = "▲" if t.is_long else "▼"
                trade_markers.append(
                    f'<text x="{ox:.1f}" y="{oy - 4:.1f}" fill="{color}" font-size="12" text-anchor="middle">{symbol}</text>'
                )

            if close_idx is not None:
                cx, cy = get_coords(close_idx, self.equity_curve[close_idx].equity)
                color = "#3B82F6" if t.is_win else "#F59E0B"
                trade_markers.append(
                    f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="{color}" stroke="#FFFFFF" stroke-width="1"/>'
                )

        markers_str = "\n".join(trade_markers)

        svg = f"""
<svg viewBox="0 0 {self.width} {self.height}" class="qs-chart equity-trade-overlay" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#1E293B" rx="8"/>
  <g class="grid" stroke="#334155" stroke-dasharray="4">
    <line x1="{padding}" y1="{padding}" x2="{self.width - padding}" y2="{padding}"/>
    <line x1="{padding}" y1="{padding + h / 2}" x2="{self.width - padding}" y2="{padding + h / 2}"/>
    <line x1="{padding}" y1="{padding + h}" x2="{self.width - padding}" y2="{padding + h}"/>
  </g>
  <polyline fill="none" stroke="#38BDF8" stroke-width="2" points="{path_str}"/>
  {markers_str}
  <text x="{padding}" y="{padding - 15}" fill="#94A3B8" font-size="12" font-weight="bold">Equity Curve ($) + Trade Entry/Exit Overlay</text>
  <text x="{self.width - padding}" y="{padding - 15}" fill="#10B981" font-size="11" text-anchor="end">▲ Long  ▼ Short  ● Exit</text>
  <text x="{padding}" y="{padding + h + 25}" fill="#64748B" font-size="10">{self.equity_curve[0].timestamp[:10]}</text>
  <text x="{self.width - padding}" y="{padding + h + 25}" fill="#64748B" font-size="10" text-anchor="end">{self.equity_curve[-1].timestamp[:10]}</text>
  <text x="{padding + 5}" y="{padding + 15}" fill="#94A3B8" font-size="10">${max_eq:,.0f}</text>
  <text x="{padding + 5}" y="{padding + h - 5}" fill="#94A3B8" font-size="10">${min_eq:,.0f}</text>
</svg>
""".strip()
        return svg


class TradePnLDistributionChart(BaseChartGenerator):
    """Generates an SVG chart showing Trade Return % distribution."""

    def __init__(self, trades: List[Trade], width: int = 800, height: int = 250):
        self.trades = trades
        self.width = width
        self.height = height

    def render_svg(self) -> str:
        if not self.trades:
            return '<div class="chart-error">Không có dữ liệu Trade Log</div>'

        padding = 40
        w = self.width - 2 * padding
        h = self.height - 2 * padding

        returns = [t.return_pct for t in self.trades]
        min_r = min(returns)
        max_r = max(returns)

        # Draw zero line y
        zero_y = padding + h - ((0.0 - min_r) / (max_r - min_r + 1e-6)) * h
        zero_y = max(padding, min(padding + h, zero_y))

        bars = []
        bar_w = max(2.0, w / len(self.trades))

        for i, t in enumerate(self.trades):
            x = padding + i * bar_w
            r = t.return_pct
            y = padding + h - ((r - min_r) / (max_r - min_r + 1e-6)) * h

            color = "#10B981" if r >= 0 else "#EF4444"
            rect_h = abs(y - zero_y)
            rect_y = min(y, zero_y)

            bars.append(f'<rect x="{x:.1f}" y="{rect_y:.1f}" width="{bar_w:.1f}" height="{rect_h:.1f}" fill="{color}"/>')

        bars_str = "\n".join(bars)

        svg = f"""
<svg viewBox="0 0 {self.width} {self.height}" class="qs-chart trade-pnl-dist" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#1E293B" rx="8"/>
  <line x1="{padding}" y1="{zero_y:.1f}" x2="{self.width - padding}" y2="{zero_y:.1f}" stroke="#94A3B8" stroke-dasharray="2"/>
  {bars_str}
  <text x="{padding}" y="{padding - 12}" fill="#94A3B8" font-size="12" font-weight="bold">Phân phối Lợi nhuận từng Giao dịch (Trade Return %)</text>
  <text x="{self.width - padding}" y="{padding - 12}" fill="#64748B" font-size="10" text-anchor="end">Tổng: {len(self.trades)} trades</text>
  <text x="{padding}" y="{padding + h + 20}" fill="#64748B" font-size="10">Max: {max_r:.2f}%</text>
  <text x="{self.width - padding}" y="{padding + h + 20}" fill="#64748B" font-size="10" text-anchor="end">Min: {min_r:.2f}%</text>
</svg>
""".strip()
        return svg
