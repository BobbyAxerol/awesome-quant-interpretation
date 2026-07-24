# -*- coding: utf-8 -*-
"""
quant_bot.analyzers.performance — Badges and KPI metric performance evaluator.
"""

from typing import Dict, Any, Optional
from ..domain.metrics import TargetThresholds, BadgeStatus
from .base import BaseAnalyzer


def to_float(val: Any) -> Optional[float]:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(",", "").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None


class PerformanceBadgeAnalyzer(BaseAnalyzer):
    """Evaluates strategy metrics against target thresholds to calculate badges."""

    def __init__(self, kpi: Dict[str, Any], targets: TargetThresholds = None):
        self.kpi = kpi
        self.targets = targets or TargetThresholds()

    def analyze(self) -> Dict[str, BadgeStatus]:
        cagr = to_float(self.kpi.get("cagrpct", ""))
        mdd = abs(to_float(self.kpi.get("max_drawdown", "")) or 0)
        pf = to_float(self.kpi.get("profit_factor", ""))

        def create_badge(metric_name: str, val: Optional[float], pass_fn, edge_fn=None) -> BadgeStatus:
            if val is None:
                return BadgeStatus(metric_name=metric_name, value=None, status="pending", label="—")
            if edge_fn and edge_fn(val):
                return BadgeStatus(metric_name=metric_name, value=val, status="edge", label="SÁT NGƯỠNG")
            if pass_fn(val):
                return BadgeStatus(metric_name=metric_name, value=val, status="pass", label="ĐẠT")
            return BadgeStatus(metric_name=metric_name, value=val, status="fail", label="CHƯA ĐẠT")

        cagr_badge = create_badge("cagr", cagr, lambda v: v >= self.targets.cagr_min)
        mdd_badge = create_badge("mdd", mdd, lambda v: v <= self.targets.mdd_max)
        pf_badge = create_badge(
            "pf", pf,
            pass_fn=lambda v: v > self.targets.pf_min,
            edge_fn=lambda v: abs(v - self.targets.pf_min) < 1e-6
        )

        return {
            "cagr": cagr_badge,
            "mdd": mdd_badge,
            "pf": pf_badge,
        }
