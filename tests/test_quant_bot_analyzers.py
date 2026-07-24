# -*- coding: utf-8 -*-
"""Unit tests for quant_bot.analyzers."""

from quant_bot.domain.trade import Trade
from quant_bot.analyzers.performance import PerformanceBadgeAnalyzer
from quant_bot.analyzers.trade_analyzer import TradeLogAnalyzer


def test_performance_badge_analyzer():
    kpi = {"cagrpct": "25.5%", "max_drawdown": "-15.0%", "profit_factor": "1.8"}
    analyzer = PerformanceBadgeAnalyzer(kpi)
    badges = analyzer.analyze()

    assert badges["cagr"].status == "pass"
    assert badges["mdd"].status == "pass"
    assert badges["pf"].status == "pass"


def test_trade_log_analyzer():
    trades = [
        Trade(
            strategy_id="S1", symbol="ETHUSDT", exchange="BINANCE", instrument_id="ETH",
            position_type="LONG", open_datetime="2020-01-01 00:00:00", close_datetime="2020-01-01 02:00:00",
            entry_price=100.0, exit_price=110.0, quantity=1.0, realized_pnl=10.0, fees=0.1,
            duration_seconds=7200, return_pct=10.0
        ),
        Trade(
            strategy_id="S1", symbol="ETHUSDT", exchange="BINANCE", instrument_id="ETH",
            position_type="SHORT", open_datetime="2020-01-02 00:00:00", close_datetime="2020-01-02 02:00:00",
            entry_price=100.0, exit_price=105.0, quantity=1.0, realized_pnl=-5.0, fees=0.1,
            duration_seconds=7200, return_pct=-5.0
        ),
    ]

    analyzer = TradeLogAnalyzer(trades)
    stats = analyzer.analyze()

    assert stats["total_trades"] == 2
    assert stats["win_count"] == 1
    assert stats["loss_count"] == 1
    assert stats["win_rate"] == 50.0
    assert stats["total_pnl"] == 5.0
    assert stats["profit_factor"] == 2.0
