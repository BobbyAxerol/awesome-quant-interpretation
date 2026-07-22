# Hướng dẫn Chi Tiết

## Mục lục
1. [Khái niệm cơ bản](#khái-niệm-cơ-bản)
2. [Cài đặt chi tiết](#cài-đặt-chi-tiết)
3. [Sử dụng từng script](#sử-dụng-từng-script)
4. [Tuỳ chỉnh ngưỡng](#tuỳ-chỉnh-ngưỡng)
5. [Troubleshooting](#troubleshooting)

## Khái niệm cơ bản

Dự án tự động hóa quá trình sinh báo cáo chiến lược định lượng từ QuantStats HTML exports. Quy trình gồm 3 bước:

### Bước 1: Rút trích dữ liệu (`qs_extract.py`)
- Đọc file HTML từ QuantStats
- Tách 12 chart SVG từ HTML
- Lấy bảng KPI, EOY data, Maximum Drawdown information
- Tự động phát hiện timeframe từ title report

### Bước 2: Phân tích & Tính badge (`qs_analyze.py`)
- So sánh metrics với ngưỡng định trước
- Sinh badge đánh giá (ĐẠT/SÁT NGƯỠNG/CHƯA ĐẠT)
- Tạo câu phân tích rule-based

### Bước 3: Ghép báo cáo (`build_report.py`)
- Nhập dữ liệu vào template HTML
- Tạo báo cáo HTML cuối cùng
- (Tùy chọn) Xuất ảnh sanity-check

## Cài đặt chi tiết

### Yêu cầu hệ thống

**Python 3.8+** (khuyến nghị 3.10+)

```bash
python3 --version
```

### Bước 1: Clone repository
```bash
git clone https://github.com/BobbyAxerol/awesome-quant-interpretation.git
cd awesome-quant-interpretation
```

### Bước 2: Tạo virtual environment (khuyến khích)
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# hoặc
venv\Scripts\activate  # Windows
```

### Bước 3: Cài đặt dependencies
```bash
pip install -e ".[dev]"
```

Điều này cài đặt:
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML processing
- `pillow` - Image rendering
- Các dev tools: `black`, `flake8`, `isort`, `pylint`, `pytest`

### Bước 4: Cài đặt optional tools
Để sử dụng `--sanity-check`:

**macOS:**
```bash
brew install librsvg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install librsvg2-bin
```

**CentOS/RHEL:**
```bash
sudo yum install librsvg2-devel
```

**Windows:**
Tải từ: https://github.com/miyako/librsvg-windows/releases

### Bước 5: Cài đặt pre-commit hooks
```bash
pre-commit install
```

Từ giờ, mỗi lần `git commit`, các checks tự động chạy.

## Sử dụng từng script

### 1. qs_extract.py - Rút trích dữ liệu

```python
from qs_extract import QuantStatsExtractor

extractor = QuantStatsExtractor("path/to/quantstats.html")
data = extractor.extract()

# data chứa:
# - data['charts']: Dict 12 chart SVG
# - data['metrics']: Dict KPI metrics
# - data['timeframe']: Detected timeframe
# - data['eoy_data']: End of year data
# - data['drawdown_table']: Drawdown analysis
```

**Thứ tự 12 charts:**
1. Cumulative Returns
2. Cumulative Returns (Log Scale)
3. Drawdown
4. Daily Returns
5. Distribution
6. Rolling Returns
7. Rolling Volatility
8. Underwater Plot
9. Monthly Returns
10. Yearly Returns
11. Volatility
12. Rolling Sharpe Ratio

Nếu QuantStats không sinh theo thứ tự này (vì bạn thêm benchmark, đổi mode, v.v.), cần update `SLOT_ORDER` trong `qs_extract.py`.

### 2. qs_analyze.py - Phân tích & Tính badge

```python
from qs_analyze import QuantStatsAnalyzer

analyzer = QuantStatsAnalyzer(data)
analysis = analyzer.analyze()

# analysis chứa:
# - analysis['badges']: Badge images (ĐẠT/SÁT NGƯỠNG/CHƯA ĐẠT)
# - analysis['comments']: Rule-based comments cho mỗi chart
# - analysis['summary']: Tóm tắt chung
```

**Ngưỡng mặc định:**
```python
TARGETS = {
    'CAGR': 20,           # %
    'MDD': -20,           # %
    'PF': 1.5,            # Profit Factor
    'Sharpe': 1.0,        # Sharpe Ratio
    'Win Rate': 50,       # %
}
```

### 3. build_report.py - Ghép báo cáo

**Cách chạy:**
```bash
python build_report.py \
    --quantstats path/to/quantstats_train.html \
    --template template.html \
    --out report_final.html \
    --sanity-check
```

**Các flag:**
- `--quantstats`: (Bắt buộc) File QuantStats train
- `--quantstats-test`: (Tùy chọn) File QuantStats test
- `--template`: (Bắt buộc) File template HTML
- `--out`: (Bắt buộc) Output path
- `--sanity-check`: (Tùy chọn) Xuất ảnh verify

**Output:**
- `report_final.html` - Báo cáo cuối cùng
- `report_final.html.sanity_check.png` (nếu `--sanity-check`) - Contact sheet 12 chart

## Tuỳ chỉnh ngưỡng

### Cách 1: Sửa trong code (permanent)

Mở `qs_analyze.py`, tìm section `TARGETS`:

```python
TARGETS = {
    'CAGR': 20,           # Đổi từ 20 thành giá trị khác
    'MDD': -20,
    'PF': 1.5,
    'Sharpe': 1.0,
    'Win Rate': 50,
}
```

### Cách 2: Pass via command line (tương lai)

Tính năng này đang được lên kế hoạch - check back sau.

## Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'bs4'"

**Solution:**
```bash
pip install beautifulsoup4
```

### ❌ "No module named 'PIL'"

**Solution:**
```bash
pip install pillow
```

### ❌ "rsvg-convert not found" (khi dùng --sanity-check)

**macOS:**
```bash
brew install librsvg
```

**Linux:**
```bash
sudo apt-get install librsvg2-bin
```

### ❌ "Chart order seems wrong in sanity-check image"

Điều này có thể xảy ra nếu:
1. Bạn dùng `quantstats.reports.html()` với benchmark
2. Bạn dùng mode khác `"full"`
3. Bạn dùng custom layout

**Solution:**
1. Mở file QuantStats HTML
2. Đếm thứ tự chart thực tế
3. Update `SLOT_ORDER` trong `qs_extract.py`
4. Chạy lại với `--sanity-check`

### ❌ "Timeframe detection failed"

Nếu script không detect được timeframe:
1. Mở file QuantStats HTML
2. Tìm title report (thường ở top page)
3. Copy timeframe text
4. Pass vào script via flag (feature tương lai) hoặc update hardcoded value

### ❌ "File xuất không có data"

Check:
1. File input HTML có valid không? (Mở bằng browser xem có chart không)
2. File template HTML có valid không?
3. Có lỗi gì trong console output?

```bash
python build_report.py ... 2>&1 | tee debug.log
```

---

**Cần giúp?** Mở issue hoặc tham gia discussions!
