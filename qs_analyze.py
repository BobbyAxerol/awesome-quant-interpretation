# -*- coding: utf-8 -*-
"""
qs_analyze.py — Sinh nhận định rule-based (không dùng LLM) từ số liệu đã trích xuất.
Toàn bộ câu chữ ở đây là template cố định, chỉ điền số — không suy diễn hình dạng chart.
"""
import re

def to_float(s: str):
    if s is None:
        return None
    s = s.strip().replace(",", "").replace("%", "")
    try:
        return float(s)
    except ValueError:
        return None

def fmt_pct(x, digits=2):
    return f"{x:.{digits}f}%"

# ---------------------------------------------------------------
# Badge cho 3 chỉ tiêu bắt buộc của đề bài (ngưỡng có thể chỉnh ở đây)
# ---------------------------------------------------------------
TARGETS = {"cagr_min": 20.0, "mdd_max": 20.0, "pf_min": 1.5}

def compute_badges(kpi: dict, targets: dict = TARGETS) -> dict:
    cagr = to_float(kpi.get("cagrpct", ""))
    mdd = abs(to_float(kpi.get("max_drawdown", "")) or 0)
    pf = to_float(kpi.get("profit_factor", ""))

    def badge(val, cmp_fn, edge_fn=None):
        if val is None:
            return "pending", "—"
        if edge_fn and edge_fn(val):
            return "edge", "SÁT NGƯỠNG"
        return ("pass", "ĐẠT") if cmp_fn(val) else ("fail", "CHƯA ĐẠT")

    cagr_cls, cagr_lbl = badge(cagr, lambda v: v >= targets["cagr_min"])
    mdd_cls, mdd_lbl = badge(mdd, lambda v: v <= targets["mdd_max"])
    pf_cls, pf_lbl = badge(pf, lambda v: v > targets["pf_min"],
                            edge_fn=lambda v: abs(v - targets["pf_min"]) < 1e-6)
    return {
        "cagr": {"value": cagr, "class": cagr_cls, "label": cagr_lbl},
        "mdd": {"value": mdd, "class": mdd_cls, "label": mdd_lbl},
        "pf": {"value": pf, "class": pf_cls, "label": pf_lbl},
    }

# ---------------------------------------------------------------
# 12 hàm sinh nhận định — mỗi hàm chỉ dùng số đã có, không đoán hình
# ---------------------------------------------------------------
def a_cumulative_return(k, eoy, dd):
    cum = kpi_get(k, "cumulative_return"); cagr = kpi_get(k, "cagrpct")
    skew = to_float(k.get("skew", "")); kurt = to_float(k.get("kurtosis", ""))
    txt = f"Cumulative Return đạt {cum}, tương đương CAGR {cagr}/năm."
    if skew is not None and kurt is not None:
        if skew > 1 and kurt > 5:
            txt += f" Skew ({skew:.2f}) và Kurtosis ({kurt:.2f}) đều cao — lợi nhuận có xu hướng tập trung vào một số giai đoạn biến động lớn hơn là tăng trưởng đều."
        else:
            txt += f" Skew ({skew:.2f}) và Kurtosis ({kurt:.2f}) ở mức vừa phải, không cho thấy phụ thuộc quá mức vào vài giai đoạn cực đoan."
    return txt

def a_cumulative_return_log(k, eoy, dd):
    if len(eoy) >= 2:
        first, last = eoy[0], eoy[-2] if len(eoy) > 1 and to_float(eoy[-1]["return"]) is not None else eoy[-1]
        r_first = to_float(first["return"]); r_last = to_float(last["return"])
        if r_first is not None and r_last is not None:
            trend = "chậm lại" if r_last < r_first else "tăng tốc"
            return (f"Return năm {first['year']} là {first['return']}%, đến năm {last['year']} còn {last['return']}% "
                    f"— tốc độ tăng trưởng theo năm {trend} so với giai đoạn đầu.")
    return "Xem thang log để đánh giá tốc độ tăng trưởng tương đối qua từng giai đoạn, tách biệt với biên độ tuyệt đối."

def a_eoy_returns(k, eoy, dd):
    rets = [to_float(r["return"]) for r in eoy if to_float(r["return"]) is not None]
    if not rets:
        return "Xem chi tiết return theo từng năm ở bảng EOY Returns bên dưới."
    win_years = sum(1 for r in rets if r > 0)
    return (f"{win_years}/{len(rets)} năm có return dương (min {min(rets):.2f}%, max {max(rets):.2f}%). "
            f"Xem bảng EOY Returns bên dưới để đối chiếu chi tiết từng năm.")

def a_monthly_dist(k, eoy, dd):
    win, loss, payoff = kpi_get(k, "avg_win"), kpi_get(k, "avg_loss"), to_float(k.get("payoff_ratio", ""))
    txt = f"Avg. Win {win} so với Avg. Loss {loss}"
    if payoff:
        txt += f" (Payoff Ratio {payoff:.2f})."
    else:
        txt += "."
    return txt

def a_daily_returns(k, eoy, dd):
    best, worst = kpi_get(k, "best_day"), kpi_get(k, "worst_day")
    sharpe, sortino = to_float(k.get("sharpe", "")), to_float(k.get("sortino", ""))
    txt = f"Best Day {best} so với Worst Day {worst}."
    if sharpe and sortino:
        gap = "cao hơn đáng kể" if sortino > sharpe * 1.3 else "gần tương đương"
        txt += f" Sortino ({sortino:.2f}) {gap} Sharpe ({sharpe:.2f}) — chênh lệch này phản ánh mức độ bất đối xứng giữa biến động dương và âm."
    return txt

def a_rolling_vol(k, eoy, dd):
    vol = kpi_get(k, "volatility_ann")
    return f"Volatility (ann.) toàn kỳ: {vol}. Đối chiếu chart để xem giai đoạn nào rolling 6 tháng vượt xa mức này."

def a_rolling_sharpe(k, eoy, dd):
    sharpe = kpi_get(k, "sharpe")
    return f"Sharpe toàn kỳ: {sharpe} — đây là giá trị trung bình; rolling 6-tháng trên chart thường dao động rộng hơn con số này, nên xem thêm biên độ dao động trước khi kết luận tính ổn định."

def a_rolling_sortino(k, eoy, dd):
    sortino = kpi_get(k, "sortino")
    return f"Sortino toàn kỳ: {sortino}. Vì Sortino chỉ phạt biến động âm, biên độ rolling thường rộng hơn Rolling Sharpe tương ứng."

def a_worst_dd_periods(k, eoy, dd):
    if not dd:
        return "Xem bảng Worst Drawdowns bên dưới để đối chiếu từng giai đoạn."
    deepest = max(dd, key=lambda r: abs(to_float(r["drawdown"]) or 0))
    longest = max(dd, key=lambda r: to_float(r["days"]) or 0)
    if deepest is longest:
        return (f"Đợt drawdown {deepest['drawdown']}% ({deepest['started']} → {deepest['recovered']}) "
                f"vừa là đợt sâu nhất vừa là đợt dài nhất ({deepest['days']} ngày).")
    return (f"Đợt lỗ sâu nhất ({deepest['drawdown']}%, {deepest['started']} → {deepest['recovered']}) "
            f"không phải đợt dài nhất — đợt dài nhất kéo {longest['days']} ngày "
            f"({longest['started']} → {longest['recovered']}, drawdown {longest['drawdown']}%).")

def a_underwater(k, eoy, dd):
    avg_dd, avg_days = kpi_get(k, "avg_drawdown"), kpi_get(k, "avg_drawdown_days")
    return f"Avg. Drawdown {avg_dd}, kéo dài trung bình {avg_days} ngày mỗi đợt."

def a_monthly_heatmap(k, eoy, dd):
    return ("Rà theo cột (cùng tháng, khác năm) để kiểm tra tính lặp lại của bất kỳ pattern mùa vụ nào "
            "qua nhiều năm trước khi kết luận đó là edge thật thay vì nhiễu ngẫu nhiên.")

def a_return_quantiles(k, eoy, dd):
    return ("Biên độ dự kiến nới rộng dần từ Daily đến Yearly theo hiệu ứng compounding — "
            "nên kiểm tra xem box Yearly có bị kéo lệch bởi 1-2 năm đầu hay phản ánh đúng mức trung bình.")

def kpi_get(k, key):
    return k.get(key, "N/A")

ANALYSIS_FUNCS = {
    "cumulative_return": a_cumulative_return,
    "cumulative_return_log": a_cumulative_return_log,
    "eoy_returns_chart": a_eoy_returns,
    "monthly_dist": a_monthly_dist,
    "daily_returns": a_daily_returns,
    "rolling_vol": a_rolling_vol,
    "rolling_sharpe": a_rolling_sharpe,
    "rolling_sortino": a_rolling_sortino,
    "worst_dd_periods": a_worst_dd_periods,
    "underwater": a_underwater,
    "monthly_heatmap": a_monthly_heatmap,
    "return_quantiles": a_return_quantiles,
}

def a_part1_summary(k, eoy, dd, badges):
    cagr_b, mdd_b, pf_b = badges["cagr"], badges["mdd"], badges["pf"]
    parts = []
    n_pass = sum(1 for b in (cagr_b, mdd_b, pf_b) if b["class"] == "pass")
    if n_pass == 3:
        parts.append("Cả 3 chỉ tiêu bắt buộc của đề bài (CAGR, MDD, Profit Factor) đều đạt ngưỡng kỳ vọng.")
    else:
        edge_or_fail = [name for name, b in [("CAGR", cagr_b), ("MDD", mdd_b), ("Profit Factor", pf_b)]
                         if b["class"] != "pass"]
        parts.append(f"Cần lưu ý khi trình bày: {', '.join(edge_or_fail)} chưa đạt rõ ràng ngưỡng kỳ vọng của đề bài (xem badge ở mục 1.2).")
    skew = to_float(k.get("skew", "")); kurt = to_float(k.get("kurtosis", ""))
    if skew is not None and kurt is not None and skew > 1 and kurt > 5:
        parts.append(f"Skew ({skew:.2f}) và Kurtosis ({kurt:.2f}) đều cao — nên chuẩn bị sẵn câu trả lời về mức độ phụ thuộc vào các giai đoạn biến động lớn (tail events), vì đây đúng là loại câu hỏi mà khung robust-check ở Phần II đang xử lý cho một chiến lược khác.")
    return " ".join(parts)

def generate_all_analysis(kpi, eoy, dd, badges=None):
    out = {slot: fn(kpi, eoy, dd) for slot, fn in ANALYSIS_FUNCS.items()}
    if badges is not None:
        out["part1_summary"] = a_part1_summary(kpi, eoy, dd, badges)
    return out

THRESHOLD_TEXT = {"cagr": "yêu cầu ~20%/năm", "mdd": "yêu cầu &lt; 20%", "pf": "yêu cầu &gt; 1.5"}

def badge_html(name, badges):
    b = badges[name]
    return f'<span class="badge {b["class"]}">{b["label"]}</span> &nbsp;{THRESHOLD_TEXT[name]}'

def pf_note_text(badges):
    b = badges["pf"]
    if b["class"] == "edge":
        return (f'Profit Factor đúng bằng {b["value"]:.2f} — về mặt kỹ thuật đề bài yêu cầu <em>lớn hơn</em> 1.5 (strict), '
                f'nên đây là ranh giới cần làm tròn cẩn thận khi trình bày; không nên tự nhận là "đã vượt yêu cầu" ở chỉ số này.')
    if b["class"] == "fail":
        return f'Profit Factor {b["value"]:.2f} đang dưới ngưỡng yêu cầu (&gt; 1.5) — cần cải thiện trước khi trình bày.'
    return f'Profit Factor {b["value"]:.2f} vượt ngưỡng yêu cầu (&gt; 1.5) một cách rõ ràng.'

def period_mismatch_html(meta, required_start_year="2018", required_end_year="2024"):
    ds, de = meta.get("date_start"), meta.get("date_end")
    if not ds or not de:
        return ""
    if required_start_year in ds and required_end_year in de:
        return ""
    return (f'<blockquote>Lưu ý: khung thời gian trong file QuantStats bạn upload ({ds} – {de}) chưa khớp với khung '
            f'01/01/{required_start_year}–31/12/{required_end_year} nêu trong đề. Nếu đây không phải là bản chạy lại theo đúng phạm vi yêu cầu, '
            f'bạn nên backtest lại đúng cửa sổ {required_start_year}–{required_end_year} trước khi nộp/thuyết trình để tránh bị hỏi ngược ở buổi phỏng vấn.</blockquote>')
    from qs_extract import extract_all
    data = extract_all("/mnt/user-data/uploads/quantstats_daily.html")
    badges = compute_badges(data["kpi"])
    print("BADGES:", badges)
    print()
    texts = generate_all_analysis(data["kpi"], data["eoy"], data["drawdowns"])
    for slot, txt in texts.items():
        print(f"[{slot}] {txt}\n")