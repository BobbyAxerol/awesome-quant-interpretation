# -*- coding: utf-8 -*-
"""
quant_bot.extractors.csv_extractor — Extractor for trade logs, equity curves, fills, and metrics.
"""

import csv
import json
import os
from typing import List, Dict, Any, Optional
from ..domain.trade import Trade, Fill, EquityPoint
from .base import BaseExtractor


class TradeLogExtractor(BaseExtractor):
    """Extractor for trade_log.csv."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> List[Trade]:
        if not os.path.exists(self.file_path):
            return []

        trades = []
        with open(self.file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                order_ids_str = row.get("order_ids", "")
                order_ids = [o.strip('" ') for o in order_ids_str.split(",") if o.strip()]
                trade = Trade(
                    strategy_id=row.get("strategy_id", ""),
                    symbol=row.get("symbol", ""),
                    exchange=row.get("exchange", ""),
                    instrument_id=row.get("instrument_id", ""),
                    position_type=row.get("position_type", ""),
                    open_datetime=row.get("open_datetime", ""),
                    close_datetime=row.get("close_datetime", ""),
                    entry_price=float(row.get("entry_price", 0.0)),
                    exit_price=float(row.get("exit_price", 0.0)),
                    quantity=float(row.get("quantity", 0.0)),
                    realized_pnl=float(row.get("realized_pnl", 0.0)),
                    fees=float(row.get("fees", 0.0)),
                    duration_seconds=float(row.get("duration_seconds", 0.0)),
                    return_pct=float(row.get("return_pct", 0.0)),
                    order_ids=order_ids,
                )
                trades.append(trade)
        return trades


class EquityCurveExtractor(BaseExtractor):
    """Extractor for equity_curve.csv."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> List[EquityPoint]:
        if not os.path.exists(self.file_path):
            return []

        points = []
        with open(self.file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pt = EquityPoint(
                    timestamp=row.get("timestamp", ""),
                    equity=float(row.get("equity", 0.0)),
                    returns=float(row.get("returns", 0.0)),
                    drawdown=float(row.get("drawdown", 0.0)),
                )
                points.append(pt)
        return points


class FillReportExtractor(BaseExtractor):
    """Extractor for fills_report.csv."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> List[Fill]:
        if not os.path.exists(self.file_path):
            return []

        fills = []
        with open(self.file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                fill = Fill(
                    trader_id=row.get("trader_id", ""),
                    strategy_id=row.get("strategy_id", ""),
                    instrument_id=row.get("instrument_id", ""),
                    venue_order_id=row.get("venue_order_id", ""),
                    side=row.get("side", ""),
                    quantity=float(row.get("quantity", 0.0)),
                    avg_price=float(row.get("avg_px", 0.0)),
                    commissions=row.get("commissions", ""),
                    ts_init=row.get("ts_init", ""),
                )
                fills.append(fill)
        return fills


class StrategyRunExtractor:
    """Convenience Extractor to parse an entire strategy run folder (e.g., report_ToTheMoon-Trainset)."""

    def __init__(self, run_dir: str):
        self.run_dir = run_dir

    def extract_all(self) -> Dict[str, Any]:
        trade_log_file = os.path.join(self.run_dir, "trade_log.csv")
        equity_file = os.path.join(self.run_dir, "equity_curve.csv")
        fills_file = os.path.join(self.run_dir, "fills_report.csv")
        metrics_file = os.path.join(self.run_dir, "metrics_summary.json")

        trades = TradeLogExtractor(trade_log_file).extract()
        equity_curve = EquityCurveExtractor(equity_file).extract()
        fills = FillReportExtractor(fills_file).extract()

        metrics_summary = {}
        if os.path.exists(metrics_file):
            with open(metrics_file, encoding="utf-8") as f:
                metrics_summary = json.load(f)

        return {
            "trades": trades,
            "equity_curve": equity_curve,
            "fills": fills,
            "metrics_summary": metrics_summary,
        }
