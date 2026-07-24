# -*- coding: utf-8 -*-
"""Unit tests for quant_bot.charts and echarts_builder."""

from quant_bot.domain.trade import Trade, EquityPoint
from quant_bot.charts.echarts_builder import EChartsBuilder


def test_echarts_builder():
    equity_curve = [
        EquityPoint(timestamp="2020-01-01 00:00:00+00:00", equity=10000.0, returns=0.0, drawdown=0.0),
        EquityPoint(timestamp="2020-01-01 01:00:00+00:00", equity=10500.0, returns=0.05, drawdown=0.0),
    ]
    trades = [
        Trade(
            strategy_id="S1", symbol="ETHUSDT", exchange="BINANCE", instrument_id="ETH",
            position_type="LONG", open_datetime="2020-01-01 00:00:00", close_datetime="2020-01-01 01:00:00",
            entry_price=100.0, exit_price=105.0, quantity=1.0, realized_pnl=500.0, fees=1.0,
            duration_seconds=3600, return_pct=5.0
        )
    ]

    builder = EChartsBuilder(equity_curve, trades)
    script = builder.generate_all_scripts()

    assert "<script>" in script
    assert "echarts.init" in script
    assert "Interactive Equity Curve" in script
