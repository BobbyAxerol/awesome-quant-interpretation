# -*- coding: utf-8 -*-
"""
quant_bot.interpreters.base — Abstract base class for AI interpretation engines.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ..domain.trade import Trade
from ..domain.metrics import BadgeStatus


class BaseInterpreter(ABC):
    """Abstract Base Class for strategy interpretation engines."""

    @abstractmethod
    def generate_analysis(
        self,
        kpi: Dict[str, Any],
        eoy: List[Dict[str, Any]],
        drawdowns: List[Dict[str, Any]],
        badges: Dict[str, BadgeStatus],
        trades: List[Trade] = None,
        trade_stats: Dict[str, Any] = None,
    ) -> Dict[str, str]:
        """Generate structured textual insights for the strategy report."""
        pass
