# -*- coding: utf-8 -*-
"""
quant_bot.interpreters.ai_interpreter — AI / LLM strategy interpretation wrapper.
"""

from typing import Dict, Any, List, Optional
from ..domain.trade import Trade
from ..domain.metrics import BadgeStatus
from .base import BaseInterpreter
from .rule_interpreter import RuleBasedStrategyInterpreter


class AIStrategyInterpreter(BaseInterpreter):
    """AI / LLM-powered Strategy Interpretation engine with fallback to Rule-based engine."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.fallback_interpreter = RuleBasedStrategyInterpreter()

    def generate_analysis(
        self,
        kpi: Dict[str, Any],
        eoy: List[Dict[str, Any]],
        drawdowns: List[Dict[str, Any]],
        badges: Dict[str, BadgeStatus],
        trades: List[Trade] = None,
        trade_stats: Dict[str, Any] = None,
    ) -> Dict[str, str]:
        # Baseline execution using rule-based engine
        analysis = self.fallback_interpreter.generate_analysis(
            kpi=kpi, eoy=eoy, drawdowns=drawdowns, badges=badges, trades=trades, trade_stats=trade_stats
        )

        # Extensible slot for LLM enhancement if API key is provided
        if self.api_key:
            # LLM API call hook could be integrated here to refine executive summary text
            pass

        return analysis
