# -*- coding: utf-8 -*-
"""
quant_bot.analyzers.base — Base abstract class for analytical engines.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseAnalyzer(ABC):
    """Abstract Base Class for analysis engines."""

    @abstractmethod
    def analyze(self) -> Any:
        """Perform analytical evaluation."""
        pass
