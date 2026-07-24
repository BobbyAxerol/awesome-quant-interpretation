# -*- coding: utf-8 -*-
"""
quant_bot.analyzers.trade_analyzer — Trade-level analytics engine.
"""

from typing import List, Dict, Any
from ..domain.trade import Trade
from .base import BaseAnalyzer


class TradeLogAnalyzer(BaseAnalyzer):
    """Analyzes trade logs to derive trade statistics."""

    def __init__(self, trades: List[Trade]):
        self.trades = trades

    def analyze(self) -> Dict[str, Any]:
        if not self.trades:
            return {"total_trades": 0}

        total_trades = len(self.trades)
        wins = [t for t in self.trades if t.is_win]
        losses = [t for t in self.trades if not t.is_win]

        win_count = len(wins)
        loss_count = len(losses)
        win_rate = round((win_count / total_trades) * 100.0, 2) if total_trades > 0 else 0.0

        long_trades = [t for t in self.trades if t.is_long]
        short_trades = [t for t in self.trades if not t.is_long]

        long_wins = [t for t in long_trades if t.is_win]
        short_wins = [t for t in short_trades if t.is_win]

        long_win_rate = round((len(long_wins) / len(long_trades)) * 100.0, 2) if long_trades else 0.0
        short_win_rate = round((len(short_wins) / len(short_trades)) * 100.0, 2) if short_trades else 0.0

        total_pnl = sum(t.realized_pnl for t in self.trades)
        total_fees = sum(t.fees for t in self.trades)
        gross_profit = sum(t.realized_pnl for t in wins)
        gross_loss = abs(sum(t.realized_pnl for t in losses))
        profit_factor = round(gross_profit / gross_loss, 2) if gross_loss > 0 else (999.0 if gross_profit > 0 else 0.0)

        avg_win = gross_profit / win_count if win_count > 0 else 0.0
        avg_loss = gross_loss / loss_count if loss_count > 0 else 0.0
        payoff_ratio = round(avg_win / avg_loss, 2) if avg_loss > 0 else 0.0

        avg_duration_hours = round(sum(t.duration_hours for t in self.trades) / total_trades, 2)

        # Streaks calculation
        max_win_streak = 0
        max_loss_streak = 0
        curr_win_streak = 0
        curr_loss_streak = 0

        for t in self.trades:
            if t.is_win:
                curr_win_streak += 1
                curr_loss_streak = 0
                max_win_streak = max(max_win_streak, curr_win_streak)
            else:
                curr_loss_streak += 1
                curr_win_streak = 0
                max_loss_streak = max(max_loss_streak, curr_loss_streak)

        return {
            "total_trades": total_trades,
            "win_count": win_count,
            "loss_count": loss_count,
            "win_rate": win_rate,
            "total_pnl": round(total_pnl, 2),
            "total_fees": round(total_fees, 2),
            "profit_factor": profit_factor,
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "payoff_ratio": payoff_ratio,
            "long_count": len(long_trades),
            "long_win_rate": long_win_rate,
            "long_pnl": round(sum(t.realized_pnl for t in long_trades), 2),
            "short_count": len(short_trades),
            "short_win_rate": short_win_rate,
            "short_pnl": round(sum(t.realized_pnl for t in short_trades), 2),
            "avg_duration_hours": avg_duration_hours,
            "max_win_streak": max_win_streak,
            "max_loss_streak": max_loss_streak,
        }
