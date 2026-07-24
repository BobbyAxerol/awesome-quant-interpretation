# -*- coding: utf-8 -*-
"""
quant_bot.domain.metrics — Performance metrics, targets, and badge domain models.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class TargetThresholds:
    cagr_min: float = 20.0
    mdd_max: float = 20.0
    pf_min: float = 1.5


@dataclass
class BadgeStatus:
    metric_name: str
    value: Optional[float]
    status: str  # pass, edge, fail, pending
    label: str   # ĐẠT, SÁT NGƯỠNG, CHƯA ĐẠT, —


@dataclass
class StrategyMetrics:
    cagr: Optional[float] = None
    max_drawdown: Optional[float] = None
    profit_factor: Optional[float] = None
    sharpe: Optional[float] = None
    sortino: Optional[float] = None
    volatility_ann: Optional[float] = None
    win_rate: Optional[float] = None
    payoff_ratio: Optional[float] = None
    raw_kpi: Dict[str, Any] = None

    def __post_init__(self):
        if self.raw_kpi is None:
            self.raw_kpi = {}
