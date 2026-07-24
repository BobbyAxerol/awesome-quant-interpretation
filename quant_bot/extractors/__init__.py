# -*- coding: utf-8 -*-
"""
quant_bot.extractors — Data extraction package.
"""

from .base import BaseExtractor
from .html_extractor import QuantStatsHTMLExtractor, SLOT_ORDER
from .csv_extractor import (
    TradeLogExtractor,
    EquityCurveExtractor,
    FillReportExtractor,
    StrategyRunExtractor,
)

__all__ = [
    "BaseExtractor",
    "QuantStatsHTMLExtractor",
    "SLOT_ORDER",
    "TradeLogExtractor",
    "EquityCurveExtractor",
    "FillReportExtractor",
    "StrategyRunExtractor",
]
