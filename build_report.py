# -*- coding: utf-8 -*-
"""
build_report.py — Tự động refresh Phần I của báo cáo từ 1 file quantstats html mới.

Cách dùng:
    python3 build_report.py --quantstats path/to/new_report.html \\
                             --template   template.html \\
                             --out        report_output.html

Câu 2 (Phần II) không bị đụng vào — script chỉ ghi đè các vùng có đánh dấu
data-slot / data-metric / data-table / data-analysis / data-field trong template.
"""
import argparse
import sys
from bs4 import BeautifulSoup

from qs_extract import extract_all
from qs_analyze import (compute_badges, generate_all_analysis, badge_html,
                         pf_note_text, period_mismatch_html, to_float)

# metric hiển thị cần abs() thay vì lấy thẳng chuỗi gốc
DERIVED_METRICS = {
    "max_drawdown_abs": lambda kpi: f'{abs(to_float(kpi.get("max_drawdown","")) or 0):.2f}%'.replace(".00%","%"),
}

def fill_metrics(soup, kpi):
    n = 0
    for el in soup.find_all(attrs={"data-metric": True}):
        key = el["data-metric"]
        if key in DERIVED_METRICS:
            el.string = DERIVED_METRICS[key](kpi)
        elif key in kpi:
            el.string = kpi[key]
        else:
            el.string = "N/A"
            print(f"  [!] Không tìm thấy metric '{key}' trong KPI table.")
        n += 1
    return n

def fill_badges(soup, badges):
    for el in soup.find_all(attrs={"data-badge": True}):
        name = el["data-badge"]
        html = badge_html(name, badges)
        el.clear()
        el.append(BeautifulSoup(html, "html.parser"))

def fill_svgs(soup, svgs):
    n = 0
    for el in soup.find_all(attrs={"data-slot": True}):
        slot = el["data-slot"]
        if slot in svgs:
            el.clear()
            el.append(BeautifulSoup(svgs[slot], "html.parser"))
            n += 1
        else:
            print(f"  [!] Không có SVG cho slot '{slot}'.")
    return n

def fill_analysis(soup, texts):
    for el in soup.find_all(attrs={"data-analysis": True}):
        key = el["data-analysis"]
        el.string = texts.get(key, "")

def fill_tables(soup, eoy, drawdowns):
    eoy_tbody = soup.find(attrs={"data-table": "eoy"})
    if eoy_tbody:
        eoy_tbody.clear()
        for r in eoy:
            tr = BeautifulSoup(
                f'<tr><td>{r["year"]}</td><td class="num">{r["return"]}%</td>'
                f'<td class="num">{r["cumulative"]}%</td></tr>', "html.parser")
            eoy_tbody.append(tr)
    dd_tbody = soup.find(attrs={"data-table": "drawdowns"})
    if dd_tbody:
        dd_tbody.clear()
        for r in drawdowns:
            tr = BeautifulSoup(
                f'<tr><td class="mono">{r["started"]}</td><td class="mono">{r["recovered"]}</td>'
                f'<td class="num">{r["drawdown"]}%</td><td class="num">{r["days"]}</td></tr>', "html.parser")
            dd_tbody.append(tr)

def fill_fields(soup, data, badges):
    meta, kpi = data["meta"], data["kpi"]
    el = soup.find(attrs={"data-field": "period_actual"})
    if el and meta.get("date_start"):
        el.string = f'{meta["date_start"]} – {meta["date_end"]}'
    el = soup.find(attrs={"data-field": "riskfree_rate"})
    if el: el.string = kpi.get("riskfree_rate", "N/A")
    el = soup.find(attrs={"data-field": "time_in_market"})
    if el: el.string = kpi.get("time_in_market", "N/A")
    el = soup.find(attrs={"data-field": "pf_note"})
    if el:
        el.clear(); el.append(BeautifulSoup(pf_note_text(badges), "html.parser"))
    el = soup.find(attrs={"data-field": "period_mismatch_note"})
    if el:
        note_html = period_mismatch_html(meta)
        el.clear()
        if note_html:
            el.append(BeautifulSoup(note_html, "html.parser"))

def main():
    ap = argparse.ArgumentParser(description="Refresh Phần I của báo cáo từ file quantstats mới.")
    ap.add_argument("--quantstats", required=True, help="Đường dẫn file html xuất từ quantstats.reports.html()")
    ap.add_argument("--template", default="template.html", help="File template gốc (có data-slot markers)")
    ap.add_argument("--out", default="report_output.html", help="File output cuối cùng")
    ap.add_argument("--sanity-check", action="store_true",
                     help="Xuất kèm 1 ảnh contact-sheet 12 chart kèm tên slot để soát nhanh bằng mắt")
    args = ap.parse_args()

    print(f"[1/5] Trích xuất dữ liệu từ {args.quantstats} ...")
    data = extract_all(args.quantstats)
    print(f"       -> {len(data['svgs'])} chart, {len(data['kpi'])} KPI, "
          f"{len(data['eoy'])} năm EOY, {len(data['drawdowns'])} dòng drawdown.")

    print("[2/5] Tính badge ĐẠT/SÁT NGƯỠNG/CHƯA ĐẠT ...")
    badges = compute_badges(data["kpi"])
    for k, v in badges.items():
        print(f"       {k}: {v['label']} ({v['value']})")

    print("[3/5] Sinh nhận định rule-based cho 12 chart + tổng kết Phần I ...")
    texts = generate_all_analysis(data["kpi"], data["eoy"], data["drawdowns"], badges)

    print(f"[4/5] Nạp template {args.template} và điền dữ liệu ...")
    with open(args.template, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    n_svg = fill_svgs(soup, data["svgs"])
    n_metric = fill_metrics(soup, data["kpi"])
    fill_badges(soup, badges)
    fill_analysis(soup, texts)
    fill_tables(soup, data["eoy"], data["drawdowns"])
    fill_fields(soup, data, badges)
    print(f"       -> đã điền {n_svg} chart, {n_metric} metric.")

    print(f"[5/5] Ghi file output -> {args.out}")
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(str(soup))

    if args.sanity_check:
        make_sanity_sheet(data["svgs"], args.out + ".sanity_check.png")

    print("Xong.")

def make_sanity_sheet(svgs, out_png):
    """Xuất 1 ảnh contact-sheet 12 chart (rsvg-convert + montage) để soát nhanh bằng mắt
    xem thứ tự slot có còn khớp thật không, trước khi tin tưởng report_output.html."""
    import subprocess, tempfile, os
    tmp = tempfile.mkdtemp()
    pngs = []
    for i, (slot, svg) in enumerate(svgs.items()):
        svg_path = os.path.join(tmp, f"{i:02d}.svg")
        png_path = os.path.join(tmp, f"{i:02d}.png")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg)
        subprocess.run(["rsvg-convert", "-w", "380", svg_path, "-o", png_path], check=True)
        subprocess.run(["convert", png_path, "-gravity", "South", "-splice", "0x22",
                         "-pointsize", "14", "-annotate", "+0+2", slot, png_path], check=True)
        pngs.append(png_path)
    subprocess.run(["montage", *pngs, "-tile", "3x4", "-geometry", "+4+4",
                     "-background", "white", out_png], check=True)
    print(f"       -> đã xuất ảnh soát nhanh: {out_png} (xem để chắc thứ tự chart còn đúng)")

if __name__ == "__main__":
    sys.exit(main())