# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- [ ] CLI arguments for custom threshold values
- [ ] Support for multiple QuantStats export formats
- [ ] Parallel processing for batch reports
- [ ] Web UI for configuration
- [ ] Docker image for easy deployment
- [ ] More report templates
- [ ] Multi-language support (Chinese, English)

## [1.0.0] - 2024-07-22

### Added
- Initial release
- Automated report generation from QuantStats HTML
- 12 chart extraction and SVG processing
- Rule-based analysis comments for each chart
- Badge generation (PASS/WARNING/FAIL)
- Sanity check image generation
- Support for optional test set data
- Pre-commit hooks setup
- Comprehensive documentation
- Contributing guidelines
- MIT License
- Pre-configured pyproject.toml

### Features
- ✅ Automatic 100% of Part I report generation
- ✅ 12 chart SVG extraction from QuantStats
- ✅ KPI/EOY/Drawdown table extraction
- ✅ Rule-based analysis generation
- ✅ PASS/WARNING/FAIL badge generation
- ✅ Optional test set support
- ✅ Sanity check image output (contact sheet)
- ✅ Timeframe auto-detection
- ✅ Comprehensive error handling

### Technical
- Python 3.8+ support
- BeautifulSoup4 for HTML parsing
- Pillow for image processing
- Black + isort + flake8 for code quality
- Pre-commit hooks integration
- pytest for testing
- Comprehensive docstrings

---

[Unreleased]: https://github.com/BobbyAxerol/awesome-quant-interpretation/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/BobbyAxerol/awesome-quant-interpretation/releases/tag/v1.0.0
