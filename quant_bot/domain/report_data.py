# -*- coding: utf-8 -*-
"""
quant_bot.domain.report_data — Complete report dataset model container.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from .trade import Trade, Fill, EquityPoint
from .metrics import StrategyMetrics, BadgeStatus


@dataclass
class ReportDataset:
    meta: Dict[str, Any] = field(default_factory=dict)
    svgs: Dict[str, str] = field(default_factory=dict)
    kpi: Dict[str, Any] = field(default_factory=dict)
    eoy: List[Dict[str, Any]] = field(default_factory=list)
    drawdowns: List[Dict[str, Any]] = field(default_factory=list)
    trades: List[Trade] = field(default_factory=list)
    equity_curve: List[EquityPoint] = field(default_factory=list)
    fills: List[Fill] = field(default_factory=list)
    metrics_summary: Dict[str, Any] = field(default_factory=dict)
    badges: Dict[str, BadgeStatus] = field(default_factory=dict)
