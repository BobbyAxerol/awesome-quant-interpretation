# -*- coding: utf-8 -*-
"""
quant_bot.charts.base — Abstract base class for chart generators.
"""

from abc import ABC, abstractmethod


class BaseChartGenerator(ABC):
    """Abstract base class for custom report chart generators."""

    @abstractmethod
    def render_svg(self) -> str:
        """Render chart as an SVG string."""
        pass
