# -*- coding: utf-8 -*-
"""
main.py — QuantStats Interpretation Bot CLI Entrypoint (v2 OOP Engine).

Examples:
    python main.py --train-dir report_ToTheMoon-Trainset --test-dir report_ToTheMoon-Testnset --out report_final.html --sanity-check
    python main.py --quantstats report_ToTheMoon-Trainset/quantstats_daily.html --out report_final.html
"""

import argparse
import os
import sys
from typing import Optional

from quant_bot.domain.report_data import ReportDataset
from quant_bot.extractors.html_extractor import QuantStatsHTMLExtractor
from quant_bot.extractors.csv_extractor import StrategyRunExtractor
from quant_bot.analyzers.performance import PerformanceBadgeAnalyzer
from quant_bot.analyzers.trade_analyzer import TradeLogAnalyzer
from quant_bot.charts.trade_overlay import EquityTradeOverlayChart, TradePnLDistributionChart
from quant_bot.interpreters.rule_interpreter import RuleBasedStrategyInterpreter
from quant_bot.renderers.html_renderer import HTMLReportRenderer
from quant_bot.renderers.sanity_checker import SanityChecker


def build_dataset(html_path: str, run_dir: Optional[str] = None) -> ReportDataset:
    html_extractor = QuantStatsHTMLExtractor(html_path)
    html_data = html_extractor.extract()

    dataset = ReportDataset(
        meta=html_data["meta"],
        svgs=html_data["svgs"],
        kpi=html_data["kpi"],
        eoy=html_data["eoy"],
        drawdowns=html_data["drawdowns"],
    )

    if run_dir and os.path.exists(run_dir):
        run_data = StrategyRunExtractor(run_dir).extract_all()
        dataset.trades = run_data.get("trades", [])
        dataset.equity_curve = run_data.get("equity_curve", [])
        dataset.fills = run_data.get("fills", [])
        dataset.metrics_summary = run_data.get("metrics_summary", {})

    badge_analyzer = PerformanceBadgeAnalyzer(dataset.kpi)
    dataset.badges = badge_analyzer.analyze()

    return dataset


def main():
    parser = argparse.ArgumentParser(
        description="QuantStats Automated Report Generator & AI Interpretation Engine (v2 OOP)"
    )
    parser.add_argument("--quantstats", help="Đường dẫn file html xuất từ quantstats.reports.html()")
    parser.add_argument("--quantstats-test", help="Đường dẫn file html quantstats của TẬP TEST")
    parser.add_argument("--train-dir", help="Đường dẫn thư mục chạy train set (chứa trade_log.csv, quantstats_daily.html, v.v.)")
    parser.add_argument("--test-dir", help="Đường dẫn thư mục chạy test set")
    parser.add_argument("--template", default="template.html", help="File template HTML gốc (mặc định: template.html)")
    parser.add_argument("--out", default="report_final.html", help="File output báo cáo HTML cuối cùng")
    parser.add_argument("--sanity-check", action="store_true", help="Xuất kèm ảnh contact-sheet kiểm tra thứ tự chart")

    parser.add_argument("--api-key", help="API Key cho AI model (như Gemini / Groq free tier API)")
    parser.add_argument("--strategy-name", default="ToTheMoon Volatility Breakout", help="Tên chiến lược giao dịch")

    args = parser.parse_args()

    # Determine train html path
    train_html = args.quantstats
    train_dir = args.train_dir

    if not train_html and train_dir:
        candidate = os.path.join(train_dir, "quantstats_daily.html")
        if os.path.exists(candidate):
            train_html = candidate

    if not train_html:
        if os.path.exists("data/report_ToTheMoon-Trainset/quantstats_daily.html"):
            train_html = "data/report_ToTheMoon-Trainset/quantstats_daily.html"
            train_dir = "data/report_ToTheMoon-Trainset"
        elif os.path.exists("report_ToTheMoon-Trainset/quantstats_daily.html"):
            train_html = "report_ToTheMoon-Trainset/quantstats_daily.html"
            train_dir = "report_ToTheMoon-Trainset"
        else:
            parser.error("Vui lòng cung cấp --quantstats hoặc --train-dir")

    print(f"[1/5] Trích xuất dữ liệu TRAIN SET từ: {train_html} ...")
    train_dataset = build_dataset(train_html, train_dir)
    train_dataset.meta["strategy_name"] = args.strategy_name

    print(f"       -> {len(train_dataset.svgs)} charts, {len(train_dataset.kpi)} KPI metrics, {len(train_dataset.trades)} trades.")

    # Determine test html path
    test_html = args.quantstats_test
    test_dir = args.test_dir

    if not test_html and test_dir:
        candidate = os.path.join(test_dir, "quantstats_daily.html")
        if os.path.exists(candidate):
            test_html = candidate

    test_dataset = None
    if test_html:
        print(f"[1b/5] Trích xuất dữ liệu TEST SET từ: {test_html} ...")
        test_dataset = build_dataset(test_html, test_dir)

    # Analyze trade log
    trade_stats = None
    if train_dataset.trades:
        print(f"[2/5] Phân tích chi tiết trade log ({len(train_dataset.trades)} giao dịch) ...")
        trade_analyzer = TradeLogAnalyzer(train_dataset.trades)
        trade_stats = trade_analyzer.analyze()

    # Custom SVG & ECharts
    custom_charts = {}
    echarts_scripts = ""
    if train_dataset.equity_curve and train_dataset.trades:
        print("[3/5] Dựng bộ biểu đồ tương tác ECharts (Equity Overlay, Long/Short, PnL Dist, Heatmap) ...")
        overlay_chart = EquityTradeOverlayChart(train_dataset.equity_curve, train_dataset.trades)
        custom_charts["equity_trade_overlay"] = overlay_chart.render_svg()

        pnl_dist_chart = TradePnLDistributionChart(train_dataset.trades)
        custom_charts["trade_pnl_distribution"] = pnl_dist_chart.render_svg()

        from quant_bot.charts.echarts_builder import EChartsBuilder
        echarts_builder = EChartsBuilder(train_dataset.equity_curve, train_dataset.trades)
        echarts_scripts = echarts_builder.generate_all_scripts()

    # Generate AI / Rule Interpretation
    print("[4/5] Sinh nhận định phân tích chiến lược (AI / Rule Engine) ...")
    from quant_bot.interpreters.ai_interpreter import AIStrategyInterpreter
    interpreter = AIStrategyInterpreter(api_key=args.api_key)
    analysis_texts = interpreter.generate_analysis(
        kpi=train_dataset.kpi,
        eoy=train_dataset.eoy,
        drawdowns=train_dataset.drawdowns,
        badges=train_dataset.badges,
        trades=train_dataset.trades,
        trade_stats=trade_stats,
    )

    # Render Report
    print(f"[5/5] Render báo cáo ra HTML -> {args.out} ...")
    renderer = HTMLReportRenderer(template_path=args.template)
    html_output = renderer.render(
        dataset=train_dataset,
        analysis_texts=analysis_texts,
        test_dataset=test_dataset,
        custom_charts=custom_charts,
        echarts_scripts=echarts_scripts,
    )

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html_output)

    if args.sanity_check:
        print("       -> Đang tạo ảnh sanity check ...")
        checker = SanityChecker(args.out + ".sanity_check.png")
        try:
            checker.generate(train_dataset.svgs)
        except Exception as e:
            print(f"[!] Sanity check bỏ qua do cảnh báo: {e}")

    print("Hoàn thành báo cáo chiến lược định lượng (v2 OOP Engine).")


if __name__ == "__main__":
    sys.exit(main())
