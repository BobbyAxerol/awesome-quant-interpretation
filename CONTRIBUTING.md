# Hướng dẫn Đóng góp

Cảm ơn bạn đã quan tâm đóng góp vào dự án! Chúng tôi rất hoan nghênh mọi hình thức đóng góp từ báo cáo bug, gợi ý tính năng, đến code improvements.

## 📋 Quy tắc cơ bản

- Hãy luôn tôn trọng những người khác
- Báo cáo bug một cách chi tiết, rõ ràng
- Trước khi bắt đầu công việc lớn, vui lòng mở một issue để thảo luận
- Tuân thủ code style của dự án

## 🐛 Báo cáo Bug

Khi báo cáo bug, vui lòng cung cấp:

1. **Mô tả chi tiết** về lỗi
2. **Bước tái hiện** (step-by-step)
3. **Kết quả mong đợi** vs **kết quả thực tế**
4. **Môi trường** (OS, Python version, dependencies versions)
5. **Thông báo lỗi** (traceback, logs)
6. **Ảnh chụp màn hình** (nếu có liên quan)

**Template:**
```
### Mô tả
[Mô tả chi tiết của bug]

### Bước tái hiện
1. [Bước 1]
2. [Bước 2]
3. ...

### Kết quả mong đợi
[Mô tả những gì nên xảy ra]

### Kết quả thực tế
[Mô tả những gì đã xảy ra]

### Môi trường
- OS: [macOS/Linux/Windows]
- Python: [version]
- beautifulsoup4: [version]
- lxml: [version]
- pillow: [version]
```

## 💡 Gợi ý Tính năng

Trước khi submit PR cho tính năng mới, vui lòng:

1. Mở một issue để thảo luận ý tưởng
2. Chờ feedback từ maintainers
3. Chắc chắn tính năng align với roadmap dự án

## 🔧 Hướng dẫn Submit PR

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/awesome-quant-interpretation.git
cd awesome-quant-interpretation
git checkout -b feature/your-feature-name
```

### 2. Cài đặt Dev Environment
```bash
pip install -e ".[dev]"
pre-commit install
```

### 3. Thực hiện Thay đổi
- Viết code theo style của dự án
- Commit message phải rõ ràng và descriptive
- Thêm tests cho code mới (nếu áp dụng)

### 4. Pre-commit Checks
```bash
# Linting & formatting sẽ chạy tự động khi commit
pre-commit run --all-files

# Hoặc chạy individual tools:
black .
isort .
flake8 .
pylint *.py
```

### 5. Push & Create PR
```bash
git push origin feature/your-feature-name
```

Rồi tạo PR trên GitHub với mô tả chi tiết về thay đổi.

## 📝 Chuẩn Code

### Python Style Guide
- Tuân thủ **PEP 8** (được kiểm soát bởi `flake8`)
- Sử dụng **Black** để format code (line length: 100)
- Sử dụng **isort** để sắp xếp imports

### Commit Messages
```
[TYPE] Short description (50 chars)

Longer description explaining the change (72 chars per line).

- Point 1
- Point 2

Fixes #123
```

**Types:**
- `feat:` - Tính năng mới
- `fix:` - Bug fix
- `docs:` - Thay đổi tài liệu
- `style:` - Formatting, không thay đổi logic
- `refactor:` - Refactor code
- `perf:` - Performance improvement
- `test:` - Thêm/sửa tests
- `chore:` - Maintenance tasks

### Ví dụ:
```
feat: Add support for custom threshold values

- Allow users to configure CAGR, MDD, PF thresholds via CLI args
- Store custom values in config file
- Add validation for threshold values

Fixes #42
```

## 🧪 Testing

Thêm tests cho code mới:

```bash
# Chạy tests
pytest

# Với coverage report
pytest --cov=.
```

## 📚 Tài liệu

Nếu thêm tính năng mới, vui lòng cập nhật:
- **README.md** - Quick start, usage examples
- **docs/guide.md** - Detailed documentation
- **Docstrings** - Function/class documentation

## ✅ Checklist trước khi Submit PR

- [ ] Code tuân thủ style guide
- [ ] Pre-commit checks pass
- [ ] Tests viết hoặc cập nhật
- [ ] README/docs cập nhật
- [ ] Commit messages rõ ràng
- [ ] Không có unrelated changes
- [ ] Branch rebase với `main` branch mới nhất

## 🎯 Development Roadmap

Xem [ROADMAP.md](docs/ROADMAP.md) để biết những tính năng đang được lên kế hoạch.

## ❓ Có Câu hỏi?

- 📖 Xem [Hướng dẫn chi tiết](docs/guide.md)
- 💬 Tham gia [Discussions](https://github.com/BobbyAxerol/awesome-quant-interpretation/discussions)
- 📧 Liên hệ maintainers

---

**Cảm ơn bạn đã đóng góp! 🙏**
