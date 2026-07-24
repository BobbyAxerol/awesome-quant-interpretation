# -*- coding: utf-8 -*-
"""
quant_bot.extractors.base — Base abstract class for data extractors.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseExtractor(ABC):
    """Abstract Base Class for strategy data extractors."""

    @abstractmethod
    def extract(self) -> Any:
        """Extract data from the source."""
        pass
