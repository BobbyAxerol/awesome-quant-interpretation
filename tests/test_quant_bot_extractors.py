# -*- coding: utf-8 -*-
"""Unit tests for quant_bot.extractors."""

import pytest
import os
from quant_bot.extractors.html_extractor import QuantStatsHTMLExtractor
from quant_bot.extractors.csv_extractor import StrategyRunExtractor


def test_html_extractor_with_real_sample():
    sample_html = "report_ToTheMoon-Trainset/quantstats_daily.html"
    if os.path.exists(sample_html):
        extractor = QuantStatsHTMLExtractor(sample_html)
        data = extractor.extract()

        assert "svgs" in data
        assert "kpi" in data
        assert "eoy" in data
        assert "drawdowns" in data
        assert len(data["svgs"]) == 12
        assert "cagrpct" in data["kpi"]


def test_csv_extractor_with_real_sample():
    sample_dir = "report_ToTheMoon-Trainset"
    if os.path.exists(sample_dir):
        extractor = StrategyRunExtractor(sample_dir)
        data = extractor.extract_all()

        assert "trades" in data
        assert "equity_curve" in data
        assert len(data["trades"]) > 0
        assert len(data["equity_curve"]) > 0
        assert data["trades"][0].position_type in ["LONG", "SHORT"]
