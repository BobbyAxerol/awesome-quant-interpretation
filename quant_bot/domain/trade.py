# -*- coding: utf-8 -*-
"""
quant_bot.domain.trade — Trade and execution domain models.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Trade:
    strategy_id: str
    symbol: str
    exchange: str
    instrument_id: str
    position_type: str  # LONG or SHORT
    open_datetime: str
    close_datetime: str
    entry_price: float
    exit_price: float
    quantity: float
    realized_pnl: float
    fees: float
    duration_seconds: float
    return_pct: float
    order_ids: List[str] = field(default_factory=list)

    @property
    def is_win(self) -> bool:
        return self.realized_pnl > 0

    @property
    def is_long(self) -> bool:
        return self.position_type.upper() == "LONG"

    @property
    def duration_hours(self) -> float:
        return round(self.duration_seconds / 3600.0, 2)


@dataclass
class Fill:
    trader_id: str
    strategy_id: str
    instrument_id: str
    venue_order_id: str
    side: str  # BUY or SELL
    quantity: float
    avg_price: float
    commissions: str
    ts_init: str


@dataclass
class EquityPoint:
    timestamp: str
    equity: float
    returns: float
    drawdown: float
