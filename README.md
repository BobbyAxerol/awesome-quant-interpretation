# QuantStats Report Generator
**Automated quantitative strategy report generation from QuantStats HTML exports**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)

Một công cụ tự động hoá sinh báo cáo chiến lược định lượng từ các file HTML xuất từ QuantStats. Tiết kiệm thời gian tái sinh báo cáo khi thay đổi alpha, timeframe hoặc dữ liệu backtest.

## 🎯 Tính năng chính

- **Tự động hóa 100%**: Rút trích 12 chart SVG, bảng KPI/EOY/Drawdown, tạo badge đánh giá
- **Phân tích rule-based**: Sinh tự động câu phân tích cho từng chart dựa trên số liệu thực tế
- **Hỗ trợ test set**: Có thể điền kết quả test riêng vào báo cáo
- **Sanity check**: Xuất ảnh contact-sheet để xác nhận lại thứ tự chart
- **Dễ sử dụng**: Chỉ cần 1 command duy nhất

## 🚀 Bắt đầu nhanh

### Yêu cầu
- Python 3.8+
- Các thư viện: `beautifulsoup4`, `lxml`, `pillow`
- (Tùy chọn) `librsvg` để render SVG → PNG

### Cài đặt

```bash
# Clone repo
git clone https://github.com/BobbyAxerol/awesome-quant-interpretation.git
cd awesome-quant-interpretation

# Cài dependencies
pip install -e ".[dev]"

# Cài pre-commit hooks
pre-commit install
```

**macOS:**
```bash
brew install librsvg
```

**Linux:**
```bash
sudo apt-get install librsvg2-bin
```

### Sử dụng

```bash
python build_report.py \
    --quantstats path/to/quantstats_train.html \
    --template template.html \
    --out report_final.html \
    --sanity-check
```

**Với test set riêng:**
```bash
python build_report.py \
    --quantstats path/to/quantstats_train.html \
    --quantstats-test path/to/quantstats_test.html \
    --template template.html \
    --out report_final.html \
    --sanity-check
```

### Các tham số

| Tham số | Bắt buộc | Mô tả |
|---------|----------|-------|
| `--quantstats` | ✅ | Đường dẫn file QuantStats HTML (train set) |
| `--quantstats-test` | ❌ | Đường dẫn file QuantStats HTML (test set) |
| `--template` | ✅ | File template HTML |
| `--out` | ✅ | Đường dẫn output |
| `--sanity-check` | ❌ | Xuất ảnh xác nhận (PNG) |

## 📋 Cấu trúc dự án

```
.
├── build_report.py         # Script chính - ghép các module và xuất báo cáo
├── qs_extract.py          # Rút trích 12 chart & bảng KPI từ QuantStats HTML
├── qs_analyze.py          # Tính badge & sinh câu phân tích rule-based
├── template.html          # Khung báo cáo - Phần II cố định, Phần I có slot trống
├── pyproject.toml         # Cấu hình Python & dependencies
├── .pre-commit-config.yaml # Cấu hình pre-commit hooks
├── README.md              # File này
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Hướng dẫn đóng góp
└── docs/                  # Tài liệu chi tiết
    ├── guide.md          # Hướng dẫn chi tiết sử dụng
    └── development.md    # Hướng dẫn phát triển
```

## 🔧 Cách hoạt động

### 1. Rút trích dữ liệu (qs_extract.py)
- Tách 12 chart SVG từ file QuantStats
- Lấy bảng KPI, EOY data, Drawdown analysis
- Tự động phát hiện timeframe từ title report

### 2. Phân tích & tính badge (qs_analyze.py)
- So sánh các chỉ số (CAGR, MDD, Profit Factor, Sharpe) với ngưỡng đặt ra
- Sinh 3 badge: ✅ ĐẠT / ⚠️ SÁT NGƯỠNG / ❌ CHƯA ĐẠT
- Tạo câu phân tích rule-based cho từng chart

### 3. Ghép báo cáo (build_report.py)
- Điền dữ liệu vào template HTML
- Tạo báo cáo cuối cùng
- (Tuỳ chọn) Xuất ảnh sanity-check

## 📊 Ngưỡng đánh giá mặc định

| Chỉ số | Ngưỡng |
|--------|--------|
| CAGR | 20% |
| Max Drawdown | 20% |
| Profit Factor | 1.5 |
| Sharpe Ratio | 1.0 |

Muốn thay đổi? Sửa biến `TARGETS` trong `qs_analyze.py`.

## ⚠️ Lưu ý quan trọng

- **Thứ tự 12 chart** giả định cố định theo QuantStats không có benchmark mode. Nếu bạn thêm benchmark hoặc đổi mode, cần update lại `SLOT_ORDER` trong `qs_extract.py`
- **Sanity-check** rất khuyến khích bật khi đổi cấu hình hoặc dữ liệu mới
- **Phần II (Câu 2)** của báo cáo không bị thay đổi tự động - sửa trực tiếp trong template hoặc file output
- **Câu phân tích** là rule-based, có thể hơi công thức - có thể copy ra sửa tay nếu cần

## 🤝 Đóng góp

Chúng tôi luôn hoan nghênh đóng góp! Xem [CONTRIBUTING.md](CONTRIBUTING.md) để biết hướng dẫn chi tiết.

**Các hình thức đóng góp:**
- 🐛 Báo cáo bug
- 💡 Gợi ý tính năng mới
- 📝 Cải thiện tài liệu
- 🔧 Submit PR

## 📚 Tài liệu thêm

- [Hướng dẫn chi tiết](docs/guide.md)
- [Hướng dẫn phát triển](docs/development.md)
- [Lịch sử thay đổi](CHANGELOG.md)

## 📄 License

MIT License - xem [LICENSE](LICENSE)

## 👥 Tác giả

- **Bobby Axerol** - Nhà sáng lập & maintainer

## 🙏 Cảm ơn

- [QuantStats](https://github.com/ranaroussi/quantstats) - Thư viện tính toán quant metrics
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Pillow](https://python-pillow.org/) - Image processing

---

**Có câu hỏi?** Mở một [issue](https://github.com/BobbyAxerol/awesome-quant-interpretation/issues) hoặc tham gia [discussions](https://github.com/BobbyAxerol/awesome-quant-interpretation/discussions).
