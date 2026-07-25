# -*- coding: utf-8 -*-
"""
quant_bot.renderers.html_renderer — HTML Report Renderer class.
"""

from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from ..domain.report_data import ReportDataset
from ..domain.metrics import BadgeStatus, TargetThresholds
from ..analyzers.performance import to_float

DERIVED_METRICS = {
    "max_drawdown_abs": lambda kpi: f'{abs(to_float(kpi.get("max_drawdown","")) or 0):.2f}%'.replace(".00%", "%"),
}

THRESHOLD_TEXT = {"cagr": "yêu cầu ~20%/năm", "mdd": "yêu cầu &lt; 20%", "pf": "yêu cầu &gt; 1.5"}


def format_badge_html(badge_name: str, badge: BadgeStatus) -> str:
    return f'<span class="badge {badge.status}">{badge.label}</span> &nbsp;{THRESHOLD_TEXT.get(badge_name, "")}'


def format_pf_note(badge: BadgeStatus) -> str:
    if badge.status == "edge":
        return (f'Profit Factor đúng bằng {badge.value:.2f} — về mặt kỹ thuật đề bài yêu cầu <em>lớn hơn</em> 1.5 (strict), '
                f'nên đây là ranh giới cần làm tròn cẩn thận khi trình bày; không nên tự nhận là "đã vượt yêu cầu" ở chỉ số này.')
    if badge.status == "fail":
        val_str = f"{badge.value:.2f}" if badge.value is not None else "N/A"
        return f'Profit Factor {val_str} đang dưới ngưỡng yêu cầu (&gt; 1.5) — cần cải thiện trước khi trình bày.'
    val_str = f"{badge.value:.2f}" if badge.value is not None else "N/A"
    return f'Profit Factor {val_str} vượt ngưỡng yêu cầu (&gt; 1.5) một cách rõ ràng.'


def format_period_mismatch_html(meta: Dict[str, Any], required_start_year: str = "2018", required_end_year: str = "2024") -> str:
    ds, de = meta.get("date_start"), meta.get("date_end")
    if not ds or not de:
        return ""
    if required_start_year in ds and required_end_year in de:
        return ""
    return (f'<blockquote>Lưu ý: khung thời gian trong file QuantStats bạn upload ({ds} – {de}) chưa khớp với khung '
            f'01/01/{required_start_year}–31/12/{required_end_year} nêu trong đề. Nếu đây không phải là bản chạy lại theo đúng phạm vi yêu cầu, '
            f'bạn nên backtest lại đúng cửa sổ {required_start_year}–{required_end_year} trước khi nộp/thuyết trình.</blockquote>')


class HTMLReportRenderer:
    """Renderer for compiling complete HTML quantitative strategy reports."""

    def __init__(self, template_path: str = "template.html"):
        self.template_path = template_path

    def render(
        self,
        dataset: ReportDataset,
        analysis_texts: Dict[str, str],
        test_dataset: Optional[ReportDataset] = None,
        custom_charts: Optional[Dict[str, str]] = None,
        echarts_scripts: Optional[str] = None,
    ) -> str:
        with open(self.template_path, encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "lxml")

        svgs = dict(dataset.svgs)
        if custom_charts:
            svgs.update(custom_charts)

        self._fill_svgs(soup, svgs)
        self._fill_metrics(soup, dataset.kpi)
        self._fill_badges(soup, dataset.badges)
        self._fill_analysis(soup, analysis_texts)
        self._fill_tables(soup, dataset.eoy, dataset.drawdowns)
        self._fill_stress_monthly(soup, dataset, is_test=False)
        self._fill_fields(soup, dataset)

        if test_dataset:
            self._fill_test_section(soup, test_dataset)
            self._fill_stress_monthly(soup, test_dataset, is_test=True)

        if echarts_scripts and soup.body:
            soup.body.append(BeautifulSoup(echarts_scripts, "html.parser"))

        return str(soup)

    def _fill_svgs(self, soup: BeautifulSoup, svgs: Dict[str, str]):
        for el in soup.find_all(attrs={"data-slot": True}):
            slot = el["data-slot"]
            if slot.startswith("test_"):
                continue
            if slot in svgs:
                el.clear()
                el.append(BeautifulSoup(svgs[slot], "html.parser"))

    def _fill_metrics(self, soup: BeautifulSoup, kpi: Dict[str, Any]):
        for el in soup.find_all(attrs={"data-metric": True}):
            key = el["data-metric"]
            if key.startswith("test_"):
                continue
            if key in DERIVED_METRICS:
                el.string = DERIVED_METRICS[key](kpi)
            elif key in kpi:
                el.string = str(kpi[key])
            else:
                el.string = "N/A"

    def _fill_badges(self, soup: BeautifulSoup, badges: Dict[str, BadgeStatus]):
        for el in soup.find_all(attrs={"data-badge": True}):
            name = el["data-badge"]
            if name.startswith("test_"):
                continue
            if name in badges:
                html = format_badge_html(name, badges[name])
                el.clear()
                el.append(BeautifulSoup(html, "html.parser"))

    def _fill_analysis(self, soup: BeautifulSoup, texts: Dict[str, str]):
        for el in soup.find_all(attrs={"data-analysis": True}):
            key = el["data-analysis"]
            if key in texts:
                el.string = texts[key]

    def _fill_tables(self, soup: BeautifulSoup, eoy: List[Dict[str, Any]], drawdowns: List[Dict[str, Any]]):
        eoy_tbody = soup.find(attrs={"data-table": "eoy"})
        if eoy_tbody:
            eoy_tbody.clear()
            for r in eoy:
                tr = BeautifulSoup(
                    f'<tr><td>{r["year"]}</td><td class="num">{r["return"]}%</td>'
                    f'<td class="num">{r["cumulative"]}%</td></tr>', "html.parser"
                )
                eoy_tbody.append(tr)

        dd_tbody = soup.find(attrs={"data-table": "drawdowns"})
        if dd_tbody:
            dd_tbody.clear()
            for r in drawdowns:
                tr = BeautifulSoup(
                    f'<tr><td class="mono">{r["started"]}</td><td class="mono">{r["recovered"]}</td>'
                    f'<td class="num">{r["drawdown"]}%</td><td class="num">{r["days"]}</td></tr>', "html.parser"
                )
                dd_tbody.append(tr)

    def _fill_stress_monthly(self, soup: BeautifulSoup, dataset: ReportDataset, is_test: bool = False):
        if not dataset.equity_curve:
            return

        from ..analyzers.stress_monthly import StressTestAnalyzer, MonthlyReturnsHeatmapBuilder
        stress_html = StressTestAnalyzer(dataset.equity_curve).render_html_table()
        monthly_html = MonthlyReturnsHeatmapBuilder(dataset.equity_curve).render_html_table()

        combined_html = f"{stress_html}\n{monthly_html}"
        container_attr = "test_stress_monthly" if is_test else "train_stress_monthly"

        el = soup.find(attrs={"data-container": container_attr})
        if el and combined_html.strip():
            el.clear()
            el.append(BeautifulSoup(combined_html, "html.parser"))

    def _fill_fields(self, soup: BeautifulSoup, dataset: ReportDataset):
        meta, kpi, badges = dataset.meta, dataset.kpi, dataset.badges

        el = soup.find(attrs={"data-field": "period_actual"})
        if el and meta.get("date_start"):
            el.string = f'{meta["date_start"]} – {meta["date_end"]}'

        el = soup.find(attrs={"data-field": "riskfree_rate"})
        if el:
            el.string = str(kpi.get("riskfree_rate", "N/A"))

        el = soup.find(attrs={"data-field": "time_in_market"})
        if el:
            el.string = str(kpi.get("time_in_market", "N/A"))

        el = soup.find(attrs={"data-field": "pf_note"})
        if el and "pf" in badges:
            el.clear()
            el.append(BeautifulSoup(format_pf_note(badges["pf"]), "html.parser"))

        el = soup.find(attrs={"data-field": "period_mismatch_note"})
        if el:
            note_html = format_period_mismatch_html(meta)
            el.clear()
            if note_html:
                el.append(BeautifulSoup(note_html, "html.parser"))

    def _fill_test_section(self, soup: BeautifulSoup, test_dataset: ReportDataset):
        svgs, kpi, test_badges = test_dataset.svgs, test_dataset.kpi, test_dataset.badges

        for el in soup.find_all(attrs={"data-slot": True}):
            test_slot = el.get("data-slot", "")
            if test_slot.startswith("test_"):
                src_slot = test_slot[5:]  # Strip 'test_' prefix
                if src_slot in svgs:
                    el.clear()
                    el.append(BeautifulSoup(svgs[src_slot], "html.parser"))

        metric_map = {
            "test_cagrpct": str(kpi.get("cagrpct", "N/A")),
            "test_max_drawdown_abs": DERIVED_METRICS["max_drawdown_abs"](kpi),
            "test_profit_factor": str(kpi.get("profit_factor", "N/A")),
            "test_sharpe": str(kpi.get("sharpe", "N/A")),
        }
        for el in soup.find_all(attrs={"data-metric": True}):
            key = el.get("data-metric")
            if key in metric_map:
                el.string = metric_map[key]

        badge_key_map = {"test_cagr": "cagr", "test_mdd": "mdd", "test_pf": "pf"}
        for el in soup.find_all(attrs={"data-badge": True}):
            name = el.get("data-badge")
            if name in badge_key_map:
                real_name = badge_key_map[name]
                if real_name in test_badges:
                    html = format_badge_html(real_name, test_badges[real_name])
                    el.clear()
                    el.append(BeautifulSoup(html, "html.parser"))
