<div align="center">

# 📊 Quant Strategy Interpretation Platform

**An Open-Source Automated Engine for Quantitative Trading Strategy Reports & AI Interpretation**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Apache ECharts](https://img.shields.io/badge/Analytics-Apache%20ECharts%205-red.svg?style=flat-square&logo=apache)](https://echarts.apache.org)
[![AI Powered](https://img.shields.io/badge/AI Engine-Gemini%20%7C%20Groq-green.svg?style=flat-square&logo=google)](https://aistudio.google.com)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-enabled-brightgreen?style=flat-square&logo=pre-commit)](https://pre-commit.com)

<p align="center">
  <a href="#-key-features">Key Features</a> •
  <a href="#-report-output-showcase">Output Showcase</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-license">License</a>
</p>

![Quant Strategy Report Banner](assets/hero_banner.png)

</div>

---

## 💡 Why Quant Interpretation Platform?

When testing algorithmic trading strategies, raw Backtrader/QuantStats metrics or CSV trade logs are often difficult for non-technical stakeholders, peers, or fund investors to interpret. 

This platform automatically extracts raw backtest runs (QuantStats HTML exports & trading logs), renders **interactive TradingView-style Apache ECharts**, builds a **2-tier dual-set report (In-Sample & Out-of-Sample)**, and enriches the final output with **free AI model insights (Google Gemini / Groq)**.

---

## ✨ Key Features

- 📈 **Interactive TradingView-Style ECharts**: 
  - **Standalone Equity Curve & Drawdown Waterfall**: High-resolution 520px equity curve paired with shaded drawdown percentage below.
  - **Market Execution Price Action Overlay**: Continuous price line connecting entry/exit points with BUY (▲ green) and SELL (▼ red) price markers.
  - **MAE / MFE Excursion Scatter**: Maximum Adverse vs Maximum Favorable Excursion for trade risk diagnosis.
  - **Account Margin & Leverage Utilization**: Balance, free margin, and used margin over time from `account_report.csv`.
  - **Long vs Short Breakdown, 30-Trade Rolling Win Rate, Return Distribution, and 2D Density Heatmap**.

- 🛡️ **2-Tier Dual-Set Architecture (Train & Test)**:
  - **Tier 1 (Primary View)**: Always-expanded interactive ECharts suites generated from backtest data.
  - **Tier 2 (Secondary View)**: Full 12 QuantStats vector SVG charts enclosed in collapsible accordions (`<details class="qs-toggle">`).

- 🤖 **Free AI Qualitative Strategy Diagnosis**:
  - Zero-dependency REST adapter supporting **Google Gemini API** (`gemini-2.5-flash`) and **Groq API** (`llama-3.3-70b`).
  - Automatically loads keys from `.env` or `--api-key` CLI flag.
  - Generates Executive Summaries, Regime Vulnerability Diagnosis, and In-Sample vs Out-of-Sample Overfitting Ratings.

- 🏆 **Dynamic KPI Threshold Badging**:
  - Automatically evaluates CAGR, Max Drawdown, Profit Factor, and Sharpe Ratio against target thresholds.
  - Displays status badges (`✅ ĐẠT`, `⚠️ SÁT NGƯỠNG`, `❌ CHƯA ĐẠT`).

- 🎨 **Publication-Grade Paper Theme Aesthetics**:
  - Styled with classic typography (`Newsreader` serif, `IBM Plex Sans`, `IBM Plex Mono`) and dark paper palette (`#F6F5F0`, `#1C3D3A`, `#B8790A`).

---

## 🎨 Report Output Showcase

![ECharts Suite & Analytics Preview](assets/echarts_suite_preview.png)

### Included Report Sections

| Section | Content & Functionality |
| :--- | :--- |
| **01. Cover & Strategy Overview** | Generalized metadata (Strategy name, Asset/Symbol, Author, Period), Executive AI summary, and Target Threshold badges. |
| **02. Core Thesis & Setup** | Collapsible breakdown of momentum signals, indicators, and risk management parameters. |
| **03. Performance Metrics** | KPI cards (CAGR, MDD, Profit Factor, Sharpe, Win Rate) + detailed metric breakdown table. |
| **04. Train Set Analytics** | **Tier 1**: 9 Interactive ECharts. **Tier 2**: Collapsible 12 QuantStats SVG Vector Charts. |
| **05. Test Set Analytics** | Out-of-Sample performance ECharts + Collapsible 12 QuantStats SVG Vector Charts. |
| **06. Degradation Analysis** | Side-by-side In-Sample vs Out-of-Sample metric comparison table & AI Overfitting Score. |

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- Dependencies: `beautifulsoup4`, `lxml`, `pillow`, `pytest`

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/BobbyAxerol/awesome-quant-interpretation.git
cd awesome-quant-interpretation

# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install package and development dependencies
pip install -e ".[dev]"
```

### 2. Environment Configuration (`.env`)

Copy `.env.example` to `.env` and add your free Google Gemini or Groq API key:

```bash
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Generate Strategy Report

Generate a report combining Train Set (In-Sample) and Test Set (Out-of-Sample) data:

```bash
python main.py \
    --train-dir data/report_ToTheMoon-Trainset \
    --test-dir data/report_ToTheMoon-Testnset \
    --out report_final.html \
    --sanity-check
```

Open `report_final.html` in your web browser!

---

## ⚙️ CLI Command Line Options

| Parameter | Required | Description |
| :--- | :---: | :--- |
| `--train-dir` | ❌ | Directory containing Train Set backtest outputs (`trade_log.csv`, `quantstats_daily.html`, etc.). |
| `--test-dir` | ❌ | Directory containing Test Set backtest outputs. |
| `--quantstats` | ❌ | Explicit path to Train Set QuantStats HTML file. |
| `--quantstats-test` | ❌ | Explicit path to Test Set QuantStats HTML file. |
| `--template` | ❌ | HTML template path (default: `template.html`). |
| `--out` | ❌ | Output report path (default: `report_final.html`). |
| `--api-key` | ❌ | Optional AI API key (Google Gemini or Groq). Reads from `.env` automatically if omitted. |
| `--sanity-check` | ❌ | Generates contact-sheet preview image (`report_final.html.sanity_check.png`). |

---

## 🏗️ Project Architecture

```
awesome-quant-interpretation/
├── quant_bot/                  # Core v2 Object-Oriented Package
│   ├── domain/                 # Domain models (Trade, Fill, EquityPoint, ReportDataset)
│   ├── extractors/             # HTML & CSV extractors (QuantStats, TradeLog, AccountHistory)
│   ├── analyzers/              # Performance & Trade Analyzers (badges, win rate, MAE/MFE)
│   ├── charts/                 # EChartsBuilder & SVG Chart Generators
│   ├── interpreters/           # AI Strategy Interpreter (Gemini / Groq) & Rule Interpreter
│   └── renderers/              # HTMLReportRenderer & SanityChecker
├── data/                       # Backtest dataset folders (Train & Test sets)
├── tests/                      # Pytest unit testing suite
├── assets/                     # README landing page assets & previews
├── template.html               # Main report HTML paper theme template
├── main.py                     # Primary CLI entrypoint & .env loader
├── .env.example                # Template for environment configuration
└── pyproject.toml              # Package dependencies & configuration
```

---

## 🧪 Testing & Verification

Run the test suite via `pytest`:

```bash
.venv/bin/pytest
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'feat: add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

---

<div align="center">
  <sub>Built with ❤️ for Quantitative Researchers & Algorithmic Traders.</sub>
</div>
