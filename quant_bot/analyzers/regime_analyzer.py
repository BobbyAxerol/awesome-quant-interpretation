# -*- coding: utf-8 -*-
"""
quant_bot.analyzers.regime_analyzer — Automated Market Regime Classification & Failure Mode Analysis.
Classifies historical backtest data into 4 market regimes, calculates multi-dimensional metrics per regime,
and generates structured RAG context for AI risk diagnosis.
"""

from collections import defaultdict
from typing import List, Dict, Any, Optional
from ..domain.trade import Trade, EquityPoint


class RegimeSensitivityAnalyzer:
    """Classifies backtest history into 4 Market Regimes and computes multi-index quant metrics."""

    def __init__(self, equity_curve: List[EquityPoint], trades: List[Trade]):
        self.equity_curve = equity_curve
        self.trades = trades

    def classify_regimes(self) -> Dict[str, Dict[str, Any]]:
        if not self.equity_curve or not self.trades:
            return {}

        # Classify trades into 4 regimes based on return & volatility
        regime_trades = defaultdict(list)
        regime_equities = defaultdict(list)

        for t in self.trades:
            ret = t.return_pct
            dur = t.duration_hours

            if ret > 4.0 and dur > 12.0:
                regime = "Bull Trend"
            elif ret < -4.0 or (t.fees / (abs(t.realized_pnl) + 1e-5) > 0.25):
                regime = "High-Vol Panic"
            elif abs(ret) <= 2.5 and dur < 8.0:
                regime = "Low-Vol Chop"
            else:
                regime = "Bear Trend"

            regime_trades[regime].append(t)

        regimes_order = ["Bull Trend", "High-Vol Panic", "Low-Vol Chop", "Bear Trend"]
        out = {}

        for reg in regimes_order:
            ts_list = regime_trades.get(reg, [])
            total = len(ts_list)
            if total == 0:
                out[reg] = {
                    "count": 0, "win_rate": 0.0, "profit_factor": 0.0,
                    "avg_hold_hours": 0.0, "fee_drag_pct": 0.0,
                    "payoff_ratio": 0.0, "max_loss_streak": 0,
                    "status": "—", "status_bg": "#F3F4F6", "status_color": "#565C63"
                }
                continue

            wins = [t for t in ts_list if t.is_win]
            losses = [t for t in ts_list if not t.is_win]

            win_rate = round((len(wins) / total) * 100.0, 1)

            win_pnl = sum(t.realized_pnl for t in wins)
            loss_pnl = abs(sum(t.realized_pnl for t in losses))
            pf = round(win_pnl / loss_pnl, 2) if loss_pnl > 0 else (round(win_pnl, 2) if win_pnl > 0 else 1.0)

            avg_hold = round(sum(t.duration_hours for t in ts_list) / total, 1)

            total_gross_profit = sum(t.realized_pnl for t in wins)
            total_fees = sum(t.fees for t in ts_list)
            fee_drag = round((total_fees / (total_gross_profit + 1e-5)) * 100.0, 1) if total_gross_profit > 0 else 100.0

            avg_win = (win_pnl / len(wins)) if wins else 0.0
            avg_loss = (loss_pnl / len(losses)) if losses else 1.0
            payoff = round(avg_win / avg_loss, 2) if avg_loss > 0 else 0.0

            # Calculate max consecutive loss streak
            max_streak = 0
            curr_streak = 0
            for t in ts_list:
                if not t.is_win:
                    curr_streak += 1
                    max_streak = max(max_streak, curr_streak)
                else:
                    curr_streak = 0

            # Determine adaptation status
            if pf >= 1.5 and win_rate >= 50.0:
                status, status_bg, status_color = "🟢 OPTIMAL", "rgba(16, 185, 129, 0.15)", "#065F46"
            elif pf >= 1.2:
                status, status_bg, status_color = "🔵 ROBUST", "rgba(59, 130, 246, 0.15)", "#1E40AF"
            elif pf >= 0.9:
                status, status_bg, status_color = "🟡 MODERATE", "rgba(245, 158, 11, 0.15)", "#92400E"
            else:
                status, status_bg, status_color = "🔴 VULNERABLE", "rgba(239, 68, 68, 0.15)", "#991B1B"

            out[reg] = {
                "count": total,
                "win_rate": win_rate,
                "profit_factor": pf,
                "avg_hold_hours": avg_hold,
                "fee_drag_pct": min(100.0, max(0.0, fee_drag)),
                "payoff_ratio": payoff,
                "max_loss_streak": max_streak,
                "status": status,
                "status_bg": status_bg,
                "status_color": status_color,
            }

        return out

    def render_html_table(self) -> str:
        regimes = self.classify_regimes()
        if not regimes:
            return ""

        rows = []
        for reg_name, d in regimes.items():
            if d["count"] == 0:
                continue

            rows.append(f"""
          <tr style="border-bottom: 1px solid var(--line-soft);">
            <td style="padding: 12px 14px; font-weight: 700; color: #181B20;">
              {reg_name}<br/>
              <span style="font-size: 11px; padding: 2px 6px; border-radius: 4px; background: {d['status_bg']}; color: {d['status_color']}; font-weight: 600; display: inline-block; margin-top: 4px;">{d['status']}</span>
            </td>
            <td style="padding: 12px 14px; font-family: var(--font-mono); font-size: 12.5px;">
              Win Rate: <strong>{d['win_rate']}%</strong><br/>
              Profit Factor: <strong>{d['profit_factor']}</strong>
            </td>
            <td style="padding: 12px 14px; font-family: var(--font-mono); font-size: 12.5px;">
              Avg Hold: <strong>{d['avg_hold_hours']}h</strong><br/>
              Fee Drag: <strong style="color: {'#AC3B34' if d['fee_drag_pct'] > 10 else '#181B20'};">{d['fee_drag_pct']}%</strong>
            </td>
            <td style="padding: 12px 14px; font-family: var(--font-mono); font-size: 12.5px;">
              Payoff Ratio: <strong>{d['payoff_ratio']}</strong><br/>
              Max Loss Streak: <strong style="color: #AC3B34;">{d['max_loss_streak']} trades</strong>
            </td>
            <td style="padding: 12px 14px; font-size: 12.5px; color: var(--ink-soft);" data-regime-ai="{reg_name}">
              <em>AI Risk Diagnosis &amp; Circuit Breaker loading...</em>
            </td>
          </tr>
""")

        html = f"""
<div class="regime-matrix-card" style="border: 1px solid var(--line); border-radius: 6px; background: #FFFFFF; margin: 24px 0; overflow: hidden; box-shadow: var(--shadow);">
  <div style="padding: 14px 18px; border-bottom: 1px solid var(--line-soft); background: var(--paper-raised);">
    <h3 style="margin: 0; font-family: var(--font-display); font-size: 15px; color: var(--ink);">Ma trận Nhạy cảm Trạng thái &amp; Phân tích Failure Modes Tự động</h3>
  </div>
  <div style="overflow-x: auto;">
    <table width="100%" style="border-collapse: collapse; font-size: 13px;">
      <thead>
        <tr style="border-bottom: 1px solid var(--line); color: var(--ink-soft); font-family: var(--font-mono); font-size: 11px; text-transform: uppercase; background: var(--paper-raised);">
          <th style="padding: 10px 14px; text-align: left; width: 18%;">Trạng thái Thị trường</th>
          <th style="padding: 10px 14px; text-align: left; width: 18%;">Hiệu năng &amp; Win Rate</th>
          <th style="padding: 10px 14px; text-align: left; width: 18%;">Chỉ số Đặc biệt</th>
          <th style="padding: 10px 14px; text-align: left; width: 18%;">Payoff &amp; Loss Streak</th>
          <th style="padding: 10px 14px; text-align: left; width: 28%;">Đánh giá Rủi ro &amp; Giải pháp Quản trị (AI Multi-Index RAG)</th>
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
