<div align="center">

# 📊 Quant Strategy Performance & Risk Analytics

**An Open-Source Automated Engine for Quantitative Trading Strategy Reports & Interactive Analytics**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Apache ECharts](https://img.shields.io/badge/Analytics-Apache%20ECharts%205-red.svg?style=flat-square&logo=apache)](https://echarts.apache.org)
[![AI Powered](https://img.shields.io/badge/AI Engine-Gemini%20%7C%20Groq-green.svg?style=flat-square&logo=google)](https://aistudio.google.com)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-enabled-brightgreen?style=flat-square&logo=pre-commit)](https://pre-commit.com)

<br/>

### 🌐 [🚀 Open Live Interactive Report (raw.githack)](https://raw.githack.com/BobbyAxerol/awesome-quant-interpretation/dev/report_final.html) &nbsp;|&nbsp; 🖥️ [GitHub Pages Demo](https://bobbyaxerol.github.io/awesome-quant-interpretation/) &nbsp;|&nbsp; 📄 [assets/report_final.html](assets/report_final.html)

<br/>

</div>

---

<!-- NATIVE HTML EMBEDDED REPORT SECTION -->
<div style="background-color: #F6F5F0; color: #181B20; padding: 24px; border-radius: 8px; border: 1px solid #DCD7CA; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">

<div style="text-align: center; margin-bottom: 20px;">
  <span style="font-size: 11px; font-weight: 600; letter-spacing: 0.1em; color: #B8790A; text-transform: uppercase;">QUANTITATIVE TRADING STRATEGY REPORT &amp; PERFORMANCE ANALYTICS</span>
  <h1 style="font-size: 26px; font-weight: 700; color: #1C3D3A; margin: 8px 0;">Quantitative Strategy Performance &amp; Risk Analytics Report</h1>
  <p style="font-size: 14px; color: #565C63; font-style: italic;">Báo cáo phân tích hiệu năng backtest, chẩn đoán rủi ro, phân phối giao dịch và đánh giá độ vững chắc trên tập In-Sample (Train) &amp; Out-of-Sample (Test).</p>
</div>

<table width="100%" style="margin-bottom: 20px; border-collapse: collapse; background: transparent;">
  <tr>
    <td style="padding: 8px; border-bottom: 1px solid #EAE7DD;"><small style="color: #8C9196; text-transform: uppercase; font-size: 10px;">TÁC GIẢ</small><br/><strong>Quant Research Team</strong></td>
    <td style="padding: 8px; border-bottom: 1px solid #EAE7DD;"><small style="color: #8C9196; text-transform: uppercase; font-size: 10px;">CHIẾN LƯỢC</small><br/><strong>Quantitative Trading Strategy</strong></td>
    <td style="padding: 8px; border-bottom: 1px solid #EAE7DD;"><small style="color: #8C9196; text-transform: uppercase; font-size: 10px;">THỊ TRƯỜNG</small><br/><strong>ETHUSDT Perpetual</strong></td>
    <td style="padding: 8px; border-bottom: 1px solid #EAE7DD;"><small style="color: #8C9196; text-transform: uppercase; font-size: 10px;">GIAI ĐOẠN</small><br/><strong>2 Jan, 2020 – 30 Dec, 2024</strong></td>
  </tr>
</table>

<blockquote style="background: #FFFFFF; border-left: 4px solid #1C3D3A; padding: 14px 18px; margin: 0 0 20px 0; border-radius: 4px;">
  <strong style="color: #1C3D3A; font-size: 12px; letter-spacing: 0.05em; text-transform: uppercase;">TÓM TẮT ĐIỀU HÀNH (AI INTERPRETATION)</strong><br/>
  <span style="font-size: 13.5px; color: #2B2F36;">Báo cáo trình bày chi tiết kết quả backtest của chiến lược giao dịch định lượng, đối chiếu với các chỉ tiêu hiệu năng cốt lõi (CAGR, Max Drawdown, Profit Factor, Sharpe Ratio), kết hợp bộ biểu đồ tương tác ECharts và phân tích nhận định chuyên sâu từ dữ liệu giao dịch thực tế.</span>
</blockquote>

<!-- HEADLINE KPIS HTML EMBED -->
<h3 style="color: #1C3D3A; border-bottom: 1px solid #DCD7CA; padding-bottom: 6px;">1.3 Headline KPIs — Đối chiếu với Ngưỡng Kỳ Vọng</h3>

<table width="100%" style="margin-bottom: 20px; border-collapse: collapse;">
  <tr text-align="center">
    <td width="33%" style="background: #FFFFFF; border: 1px solid #DCD7CA; padding: 16px; border-radius: 6px; text-align: center;">
      <small style="color: #8C9196; text-transform: uppercase; font-size: 10px;">CAGR</small><br/>
      <span style="font-size: 28px; font-weight: 700; color: #1C3D3A;">45.83%</span><br/>
      <span style="background: #E6F4EA; color: #137333; font-size: 11px; padding: 2px 8px; border-radius: 12px; font-weight: 600;">✅ ĐẠT</span> <small style="color: #565C63;">yêu cầu ~20%/năm</small>
    </td>
    <td width="33%" style="background: #FFFFFF; border: 1px solid #DCD7CA; padding: 16px; border-radius: 6px; text-align: center;">
      <small style="color: #8C9196; text-transform: uppercase; font-size: 10px;">MAX DRAWDOWN</small><br/>
      <span style="font-size: 28px; font-weight: 700; color: #1C3D3A;">11.44%</span><br/>
      <span style="background: #E6F4EA; color: #137333; font-size: 11px; padding: 2px 8px; border-radius: 12px; font-weight: 600;">✅ ĐẠT</span> <small style="color: #565C63;">yêu cầu &lt; 20%</small>
    </td>
    <td width="33%" style="background: #FFFFFF; border: 1px solid #DCD7CA; padding: 16px; border-radius: 6px; text-align: center;">
      <small style="color: #8C9196; text-transform: uppercase; font-size: 10px;">PROFIT FACTOR</small><br/>
      <span style="font-size: 28px; font-weight: 700; color: #1C3D3A;">1.56</span><br/>
      <span style="background: #E6F4EA; color: #137333; font-size: 11px; padding: 2px 8px; border-radius: 12px; font-weight: 600;">✅ ĐẠT</span> <small style="color: #565C63;">yêu cầu &gt; 1.5</small>
    </td>
  </tr>
</table>

<!-- EXTENDED METRICS TABLE EMBED -->
<table width="100%" style="font-size: 13px; border-collapse: collapse; background: #FFFFFF; border: 1px solid #DCD7CA; border-radius: 6px; margin-bottom: 20px;">
  <thead>
    <tr style="background: #EAE7DD; color: #1C3D3A;">
      <th style="padding: 10px; text-align: left;">NHÓM CHỈ SỐ</th>
      <th style="padding: 10px; text-align: left;">METRIC</th>
      <th style="padding: 10px; text-align: right;">IN-SAMPLE (TRAIN)</th>
      <th style="padding: 10px; text-align: right;">OUT-OF-SAMPLE (TEST)</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom: 1px solid #EAE7DD;">
      <td rowspan="4" style="padding: 10px; font-weight: 600; background: #F6F5F0;">Lợi nhuận</td>
      <td style="padding: 10px;">Cumulative Return (toàn kỳ)</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">559.48%</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">182.35%</td>
    </tr>
    <tr style="border-bottom: 1px solid #EAE7DD;">
      <td style="padding: 10px;">Best Year</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">82.07%</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">41.20%</td>
    </tr>
    <tr style="border-bottom: 1px solid #EAE7DD;">
      <td style="padding: 10px;">Worst Year</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">11.01%</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">5.12%</td>
    </tr>
    <tr style="border-bottom: 1px solid #EAE7DD;">
      <td style="padding: 10px;">CAGR (%/năm)</td>
      <td style="padding: 10px; text-align: right; font-family: monospace; font-weight: 600;">45.83%</td>
      <td style="padding: 10px; text-align: right; font-family: monospace; font-weight: 600;">28.40%</td>
    </tr>
    <tr style="border-bottom: 1px solid #EAE7DD;">
      <td rowspan="3" style="padding: 10px; font-weight: 600; background: #F6F5F0;">Rủi ro</td>
      <td style="padding: 10px;">Volatility (ann.)</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">20.94%</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">24.15%</td>
    </tr>
    <tr style="border-bottom: 1px solid #EAE7DD;">
      <td style="padding: 10px;">Max Drawdown (%)</td>
      <td style="padding: 10px; text-align: right; font-family: monospace; font-weight: 600;">-11.44%</td>
      <td style="padding: 10px; text-align: right; font-family: monospace; font-weight: 600;">-14.20%</td>
    </tr>
    <tr style="border-bottom: 1px solid #EAE7DD;">
      <td style="padding: 10px;">Profit Factor</td>
      <td style="padding: 10px; text-align: right; font-family: monospace; font-weight: 600;">1.56</td>
      <td style="padding: 10px; text-align: right; font-family: monospace; font-weight: 600;">1.38</td>
    </tr>
    <tr>
      <td style="padding: 10px; font-weight: 600; background: #F6F5F0;">Risk-Adjusted</td>
      <td style="padding: 10px;">Sharpe Ratio</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">1.91</td>
      <td style="padding: 10px; text-align: right; font-family: monospace;">1.42</td>
    </tr>
  </tbody>
</table>

<!-- COLLAPSIBLE DETAILS EMBED: METHODOLOGY -->
<details open style="background: #FFFFFF; border: 1px solid #DCD7CA; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
  <summary style="font-weight: 600; color: #1C3D3A; cursor: pointer;">1.2 Ý tưởng Cốt lõi &amp; Nguyên lý Tín hiệu (Click to Toggle)</summary>
  <p style="font-size: 13.5px; color: #565C63; margin-top: 10px;">
    Phần lớn tín hiệu động lượng trong crypto đối mặt một đánh đổi cố hữu: vi phân trực tiếp để đo tốc độ đổi hướng sẽ khuếch đại nhiễu tần số cao; còn làm mượt theo kiểu tích luỹ quá khứ (như EMA) lại tạo độ trễ pha, khiến tín hiệu đến sau khi cơ hội đã trôi qua.<br/><br/>
    Cách tiếp cận của chiến lược là chuyển bài toán từ "làm mượt chuỗi thời gian" sang "khớp hình học cục bộ": thay vì đo độ dốc trên từng cặp nến, ta lấy một cửa sổ gần nhất, dựng một mô hình đa thức bậc thấp đại diện cho lõi chuyển động, rồi đọc đạo hàm ngay tại biên phải của cửa sổ.
  </p>
</details>

<!-- COLLAPSIBLE DETAILS EMBED: TRAIN SET ECHARTS & QUANTSTATS -->
<details open style="background: #FFFFFF; border: 1px solid #DCD7CA; border-radius: 6px; padding: 14px 18px; margin-bottom: 16px;">
  <summary style="font-weight: 600; color: #1C3D3A; cursor: pointer;">1.4 In-Sample Performance Analytics — Train Set (ECharts Suite &amp; QuantStats Vector Charts)</summary>
  <p style="font-size: 13.5px; color: #565C63; margin-top: 10px;">
    Bộ biểu đồ bao gồm 9 ECharts tương tác (Standalone Equity 520px, Price Action &amp; Trade Signal Overlay, Long vs Short Breakdown, MAE/MFE Excursion Scatter, Account Margin Utilization, 2D Density Heatmap) và 12 biểu đồ QuantStats Vector SVG gốc.
  </p>
</details>

</div>
<!-- END NATIVE HTML EMBEDDED REPORT SECTION -->

---

## 💡 Why Quant Interpretation Platform?

When backtesting algorithmic trading strategies, raw backtest logs or static metrics are often difficult for non-technical stakeholders, peers, or fund investors to digest. 

This platform automatically extracts raw backtest runs (QuantStats HTML & trade logs), renders **interactive TradingView-style Apache ECharts**, builds a **2-tier dual-set report (In-Sample & Out-of-Sample)**, and enriches the final output with **free AI model insights (Google Gemini / Groq)**.

---

## ✨ Key Features

- 📊 **TradingView-Style ECharts Analytics Suite**:
  - **Standalone Equity Curve**: 520px high equity curve with drawdown waterfall below.
  - **Continuous Price Action Overlay**: Execution price line with BUY (▲) and SELL (▼) fill markers and `dataZoom` timeline sliders.
  - **MAE / MFE Risk Distribution**: Maximum Adverse vs Favorable Excursion scatter plots.
  - **Account Margin Utilization**: Equity vs Free Margin over time from `account_report.csv`.
  - **Long vs Short Breakdown, 30-Trade Rolling Win Rate, Return Distribution, and 2D Density Heatmap**.

- 🛡️ **2-Tier Dual-Set Architecture (Train & Test)**:
  - **Tier 1 (Primary View)**: Always-expanded interactive ECharts suites generated from backtest data.
  - **Tier 2 (Secondary View)**: Full 12 QuantStats vector SVG charts enclosed in collapsible accordions (`<details class="qs-toggle">`).

- 🤖 **Free AI Qualitative Strategy Diagnosis**:
  - Zero-dependency REST adapter supporting **Google Gemini API** (`gemini-2.5-flash`) and **Groq API** (`llama-3.3-70b`).
  - Automatically loads keys from `.env` or `--api-key` CLI flag.
  - Generates Executive Summaries, Regime Vulnerability Diagnosis, and In-Sample vs Out-of-Sample Overfitting Ratings.

- 🏆 **Dynamic KPI Threshold Badging**:
  - Automatically evaluates CAGR, Max Drawdown, Profit Factor, and Sharpe Ratio against target benchmarks with visual status badges (`✅ ĐẠT`, `⚠️ SÁT NGƯỠNG`, `❌ CHƯA ĐẠT`).

- 🎨 **Publication-Grade Paper Theme**:
  - Styled with classic typography (`Newsreader` serif, `IBM Plex Sans`, `IBM Plex Mono`) and dark paper palette (`#F6F5F0`, `#1C3D3A`, `#B8790A`).

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
├── assets/                     # README landing page marketing screenshots & assets
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
