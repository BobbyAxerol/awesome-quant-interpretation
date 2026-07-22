# Hướng dẫn Phát triển

## Cấu trúc Project

```
.
├── build_report.py              # Script chính - orchestrator
├── qs_extract.py                # Module 1: Rút trích dữ liệu từ QuantStats HTML
├── qs_analyze.py                # Module 2: Phân tích metrics & tạo comments
├── template.html                # HTML template
├── tests/                        # Unit tests
│   ├── __init__.py
│   ├── test_qs_extract.py
│   ├── test_qs_analyze.py
│   └── test_build_report.py
├── pyproject.toml               # Project metadata & dependencies
├── .pre-commit-config.yaml      # Pre-commit hooks config
├── .gitignore                   # Git ignore rules
├── README.md                    # Project README
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guide
└── docs/                        # Documentation
    ├── guide.md                 # User guide
    └── development.md           # This file
```

## Setup Dev Environment

### 1. Clone & Install

```bash
git clone https://github.com/BobbyAxerol/awesome-quant-interpretation.git
cd awesome-quant-interpretation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### 2. Verify Installation

```bash
python3 -c "import bs4, lxml, PIL; print('OK')"
which black flake8 isort pylint pytest
```

## Code Style

### Running Formatters & Linters

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Check code style with flake8
flake8 .

# Run pylint
pylint *.py

# Or run all at once
pre-commit run --all-files
```

### Style Guidelines

- **Line length**: 100 characters (enforced by Black)
- **Python version**: 3.8+ (check with `sys.version_info`)
- **Imports**: Sorted by isort (black profile)
- **Docstrings**: Use triple quotes, descriptive
- **Type hints**: Recommended but not enforced

### Example Code Style

```python
"""Module docstring - one line summary."""

import os
from pathlib import Path
from typing import Dict, List, Optional

import beautifulsoup4 as bs4
from bs4 import BeautifulSoup


def extract_charts(html_path: str) -> Dict[str, str]:
    """Extract SVG charts from QuantStats HTML.
    
    Args:
        html_path: Path to QuantStats HTML file
        
    Returns:
        Dictionary mapping chart names to SVG strings
        
    Raises:
        FileNotFoundError: If HTML file doesn't exist
    """
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"File not found: {html_path}")
    
    with open(html_path) as f:
        soup = BeautifulSoup(f, 'lxml')
    
    charts = {}
    # Implementation here...
    return charts
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_qs_extract.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_extract"
```

### Writing Tests

Create tests in `tests/` directory. Example structure:

```python
"""Tests for qs_extract module."""

import pytest
from qs_extract import QuantStatsExtractor


class TestQuantStatsExtractor:
    """Test cases for QuantStatsExtractor class."""
    
    @pytest.fixture
    def sample_html(self):
        """Provide sample HTML for testing."""
        return """<html>...</html>"""
    
    def test_extract_charts(self, sample_html):
        """Test chart extraction."""
        extractor = QuantStatsExtractor(sample_html)
        charts = extractor.extract()
        
        assert len(charts) == 12
        assert all(isinstance(v, str) for v in charts.values())
    
    def test_invalid_html(self):
        """Test handling of invalid HTML."""
        with pytest.raises(ValueError):
            extractor = QuantStatsExtractor("<invalid>")
            extractor.extract()
```

## Git Workflow

### Branch Naming

```
feature/description          - New feature
fix/description              - Bug fix
docs/description             - Documentation
refactor/description         - Code refactoring
perf/description             - Performance improvement
test/description             - Adding/fixing tests
```

### Commit Messages

```
[TYPE] Short description (50 chars)

Optional longer description explaining the change
(72 chars per line).

- Point 1
- Point 2

Fixes #123
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting (no logic changes)
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `test:` - Tests
- `chore:` - Maintenance

### Example Workflow

```bash
# Create feature branch
git checkout -b feature/cli-args

# Make changes and commit
echo "code change" >> file.py
git add .
git commit -m "feat: Add CLI argument support

- Accept threshold values via command line
- Add validation for argument values
- Update help text

Closes #42"

# Push and create PR
git push origin feature/cli-args
```

## Module Documentation

### qs_extract.py

Rut trích dữ liệu từ QuantStats HTML.

**Main Class:** `QuantStatsExtractor`

```python
class QuantStatsExtractor:
    def __init__(self, html_path: str)
    def extract(self) -> Dict
```

**SLOT_ORDER constant:**
Định nghĩa thứ tự 12 charts. Nếu QuantStats thay đổi layout, cần update ở đây.

### qs_analyze.py

Phân tích metrics và tạo comments.

**Main Class:** `QuantStatsAnalyzer`

```python
class QuantStatsAnalyzer:
    def __init__(self, data: Dict)
    def analyze(self) -> Dict
```

**TARGETS constant:**
Định nghĩa ngưỡng đánh giá. Có thể tuỳ chỉnh ở đây.

### build_report.py

Script chính - ghép các module lại.

**Main Function:** `build_report()`

Gọi `qs_extract` → `qs_analyze` → tạo HTML output.

## Debugging

### Enable Debug Output

```bash
# Print debug info to console
python build_report.py --verbose ...

# Save debug log to file
python build_report.py ... 2>&1 | tee debug.log
```

### Python Debugger

```python
import pdb

def problematic_function():
    pdb.set_trace()  # Execution will stop here
    # Now you can inspect variables, step through code, etc.
```

### Common Issues

1. **Chart order mismatch** → Check `SLOT_ORDER` in `qs_extract.py`
2. **Metrics not found** → Verify QuantStats HTML structure
3. **Template incompatible** → Check template HTML has all required placeholders
4. **Memory error on large HTML** → Process in chunks (feature request?)

## Performance Tips

- Use `lxml` parser (faster than default `html.parser`)
- Cache extracted SVG strings
- Process large reports in batches
- Consider async processing for multiple reports

## Adding New Features

### Example: Add CLI Arguments for Thresholds

1. **Update `build_report.py`:**
   ```python
   import argparse
   
   parser.add_argument('--cagr-threshold', type=float, default=20)
   parser.add_argument('--mdd-threshold', type=float, default=20)
   ```

2. **Update `qs_analyze.py`:**
   ```python
   def __init__(self, data, cagr_threshold=20, mdd_threshold=20):
       self.targets = {
           'CAGR': cagr_threshold,
           'MDD': -abs(mdd_threshold),
           # ...
       }
   ```

3. **Add tests:**
   ```python
   def test_custom_thresholds():
       analyzer = QuantStatsAnalyzer(data, cagr_threshold=30)
       assert analyzer.targets['CAGR'] == 30
   ```

4. **Update docs** in `README.md` and `docs/guide.md`

## Resources

- [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Pre-commit Framework](https://pre-commit.com/)

## Getting Help

- 💬 Ask in [Discussions](https://github.com/BobbyAxerol/awesome-quant-interpretation/discussions)
- 🐛 Report bugs in [Issues](https://github.com/BobbyAxerol/awesome-quant-interpretation/issues)
- 📖 Read [User Guide](guide.md)

---

Happy coding! 🚀
