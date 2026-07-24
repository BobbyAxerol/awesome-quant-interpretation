# -*- coding: utf-8 -*-
"""
quant_bot.interpreters.rule_interpreter — Rule-based strategy interpretation engine.
"""

from typing import Dict, Any, List, Optional
from ..domain.trade import Trade
from ..domain.metrics import BadgeStatus
from ..analyzers.performance import to_float
from .base import BaseInterpreter


def kpi_get(k: Dict[str, Any], key: str) -> str:
    return str(k.get(key, "N/A"))


class RuleBasedStrategyInterpreter(BaseInterpreter):
    """Generates rule-based quantitative strategy analysis text for report slots and summaries."""

    def generate_analysis(
        self,
        kpi: Dict[str, Any],
        eoy: List[Dict[str, Any]],
        drawdowns: List[Dict[str, Any]],
        badges: Dict[str, BadgeStatus],
        trades: List[Trade] = None,
        trade_stats: Dict[str, Any] = None,
    ) -> Dict[str, str]:
        out = {
            "cumulative_return": self._a_cumulative_return(kpi),
            "cumulative_return_log": self._a_cumulative_return_log(eoy),
            "eoy_returns_chart": self._a_eoy_returns(eoy),
            "monthly_dist": self._a_monthly_dist(kpi),
            "daily_returns": self._a_daily_returns(kpi),
            "rolling_vol": self._a_rolling_vol(kpi),
            "rolling_sharpe": self._a_rolling_sharpe(kpi),
            "rolling_sortino": self._a_rolling_sortino(kpi),
            "worst_dd_periods": self._a_worst_dd_periods(drawdowns),
            "underwater": self._a_underwater(kpi),
            "monthly_heatmap": self._a_monthly_heatmap(),
            "return_quantiles": self._a_return_quantiles(),
            "part1_summary": self._a_part1_summary(kpi, badges, trade_stats),
            "trade_execution_summary": self._a_trade_execution_summary(trade_stats),
            "echart_equity_summary": self._a_echart_equity_summary(kpi),
            "echart_price_signals_summary": self._a_echart_price_signals_summary(trade_stats),
            "echart_long_short_summary": self._a_echart_long_short_summary(trade_stats),
            "echart_mae_mfe_summary": self._a_echart_mae_mfe_summary(trade_stats),
            "echart_account_margin_summary": self._a_echart_account_margin_summary(kpi),
        }
        return out

    def _a_cumulative_return(self, k: Dict[str, Any]) -> str:
        cum = kpi_get(k, "cumulative_return")
        cagr = kpi_get(k, "cagrpct")
        skew = to_float(k.get("skew", ""))
        kurt = to_float(k.get("kurtosis", ""))
        txt = f"Cumulative Return đạt {cum}, tương đương CAGR {cagr}/năm."
        if skew is not None and kurt is not None:
            if skew > 1 and kurt > 5:
                txt += f" Skew ({skew:.2f}) và Kurtosis ({kurt:.2f}) đều cao — lợi nhuận có xu hướng tập trung vào một số giai đoạn biến động lớn hơn là tăng trưởng đều."
            else:
                txt += f" Skew ({skew:.2f}) và Kurtosis ({kurt:.2f}) ở mức vừa phải, không cho thấy phụ thuộc quá mức vào vài giai đoạn cực đoan."
        return txt

    def _a_cumulative_return_log(self, eoy: List[Dict[str, Any]]) -> str:
        if len(eoy) >= 2:
            first, last = eoy[0], eoy[-2] if len(eoy) > 1 and to_float(eoy[-1]["return"]) is not None else eoy[-1]
            r_first = to_float(first["return"])
            r_last = to_float(last["return"])
            if r_first is not None and r_last is not None:
                trend = "chậm lại" if r_last < r_first else "tăng tốc"
                return (f"Return năm {first['year']} là {first['return']}%, đến năm {last['year']} còn {last['return']}% "
                        f"— tốc độ tăng trưởng theo năm {trend} so với giai đoạn đầu.")
        return "Xem thang log để đánh giá tốc độ tăng trưởng tương đối qua từng giai đoạn, tách biệt với biên độ tuyệt đối."

    def _a_eoy_returns(self, eoy: List[Dict[str, Any]]) -> str:
        rets = [to_float(r["return"]) for r in eoy if to_float(r["return"]) is not None]
        if not rets:
            return "Xem chi tiết return theo từng năm ở bảng EOY Returns bên dưới."
        win_years = sum(1 for r in rets if r > 0)
        return (f"{win_years}/{len(rets)} năm có return dương (min {min(rets):.2f}%, max {max(rets):.2f}%). "
                f"Xem bảng EOY Returns bên dưới để đối chiếu chi tiết từng năm.")

    def _a_monthly_dist(self, k: Dict[str, Any]) -> str:
        win, loss, payoff = kpi_get(k, "avg_win"), kpi_get(k, "avg_loss"), to_float(k.get("payoff_ratio", ""))
        txt = f"Avg. Win {win} so với Avg. Loss {loss}"
        if payoff:
            txt += f" (Payoff Ratio {payoff:.2f})."
        else:
            txt += "."
        return txt

    def _a_daily_returns(self, k: Dict[str, Any]) -> str:
        best, worst = kpi_get(k, "best_day"), kpi_get(k, "worst_day")
        sharpe, sortino = to_float(k.get("sharpe", "")), to_float(k.get("sortino", ""))
        txt = f"Best Day {best} so với Worst Day {worst}."
        if sharpe and sortino:
            gap = "cao hơn đáng kể" if sortino > sharpe * 1.3 else "gần tương đương"
            txt += f" Sortino ({sortino:.2f}) {gap} Sharpe ({sharpe:.2f}) — chênh lệch này phản ánh mức độ bất đối xứng giữa biến động dương và âm."
        return txt

    def _a_rolling_vol(self, k: Dict[str, Any]) -> str:
        vol = kpi_get(k, "volatility_ann")
        return f"Volatility (ann.) toàn kỳ: {vol}. Đối chiếu chart để xem giai đoạn nào rolling 6 tháng vượt xa mức này."

    def _a_rolling_sharpe(self, k: Dict[str, Any]) -> str:
        sharpe = kpi_get(k, "sharpe")
        return f"Sharpe toàn kỳ: {sharpe} — đây là giá trị trung bình; rolling 6-tháng trên chart thường dao động rộng hơn con số này."

    def _a_rolling_sortino(self, k: Dict[str, Any]) -> str:
        sortino = kpi_get(k, "sortino")
        return f"Sortino toàn kỳ: {sortino}. Vì Sortino chỉ phạt biến động âm, biên độ rolling thường rộng hơn Rolling Sharpe tương ứng."

    def _a_worst_dd_periods(self, dd: List[Dict[str, Any]]) -> str:
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

    def _a_underwater(self, k: Dict[str, Any]) -> str:
        avg_dd, avg_days = kpi_get(k, "avg_drawdown"), kpi_get(k, "avg_drawdown_days")
        return f"Avg. Drawdown {avg_dd}, kéo dài trung bình {avg_days} ngày mỗi đợt."

    def _a_monthly_heatmap(self) -> str:
        return ("Rà theo cột (cùng tháng, khác năm) để kiểm tra tính lặp lại của bất kỳ pattern mùa vụ nào "
                "qua nhiều năm trước khi kết luận đó là edge thật thay vì nhiễu ngẫu nhiên.")

    def _a_return_quantiles(self) -> str:
        return ("Biên độ dự kiến nới rộng dần từ Daily đến Yearly theo hiệu ứng compounding — "
                "nên kiểm tra xem box Yearly có bị kéo lệch bởi 1-2 năm đầu hay phản ánh đúng mức trung bình.")

    def _a_part1_summary(self, k: Dict[str, Any], badges: Dict[str, BadgeStatus], trade_stats: Optional[Dict[str, Any]]) -> str:
        parts = []
        n_pass = sum(1 for b in badges.values() if b.status == "pass")
        if n_pass == 3:
            parts.append("Cả 3 chỉ tiêu bắt buộc của đề bài (CAGR, MDD, Profit Factor) đều đạt ngưỡng kỳ vọng.")
        else:
            edge_or_fail = [name.upper() for name, b in badges.items() if b.status != "pass"]
            parts.append(f"Cần lưu ý khi trình bày: {', '.join(edge_or_fail)} chưa đạt rõ ràng ngưỡng kỳ vọng của đề bài.")

        skew = to_float(k.get("skew", ""))
        kurt = to_float(k.get("kurtosis", ""))
        if skew is not None and kurt is not None and skew > 1 and kurt > 5:
            parts.append(f"Skew ({skew:.2f}) và Kurtosis ({kurt:.2f}) đều cao — nên chuẩn bị sẵn câu trả lời về mức độ phụ thuộc vào tail events.")

        if trade_stats and trade_stats.get("total_trades", 0) > 0:
            parts.append(
                f" Phân tích {trade_stats['total_trades']} lệnh giao dịch: Tỷ lệ thắng {trade_stats['win_rate']}%, "
                f"Profit Factor {trade_stats['profit_factor']}, thời gian nắm giữ trung bình {trade_stats['avg_duration_hours']} giờ/lệnh."
            )

        return " ".join(parts)

    def _a_trade_execution_summary(self, trade_stats: Optional[Dict[str, Any]]) -> str:
        if not trade_stats or trade_stats.get("total_trades", 0) == 0:
            return "Không có dữ liệu chi tiết trade log."

        return (
            f"Tổng số giao dịch thực thi: {trade_stats['total_trades']} (Long: {trade_stats['long_count']} lệnh, Win Rate {trade_stats['long_win_rate']}%; "
            f"Short: {trade_stats['short_count']} lệnh, Win Rate {trade_stats['short_win_rate']}%). "
            f"Tổng phí giao dịch đã trả: ${trade_stats['total_fees']:,.2f}. "
            f"Chuỗi thắng dài nhất: {trade_stats['max_win_streak']} lệnh, Chuỗi thua dài nhất: {trade_stats['max_loss_streak']} lệnh."
        )

    def _a_echart_equity_summary(self, k: Dict[str, Any]) -> str:
        cagr = kpi_get(k, "cagrpct")
        mdd = kpi_get(k, "max_drawdown")
        return f"Đường cong tài sản thể hiện mức tăng trưởng tích lũy CAGR {cagr}% đi kèm mức sụt giảm tài sản lớn nhất Max Drawdown {mdd}%. Khoảng tăng trưởng chính tập trung ở các giai đoạn biến động mạnh."

    def _a_echart_price_signals_summary(self, trade_stats: Optional[Dict[str, Any]]) -> str:
        if not trade_stats:
            return "Đồ thị thể hiện các điểm khớp lệnh thực tế (Mua / Bán) đè lên đường giá thị trường."
        return f"Chiến lược thực thi tổng cộng {trade_stats.get('total_trades', 0)} lệnh giao dịch. Các điểm tín hiệu Mua (▲ Long) và Bán (▼ Short) phản ánh chính xác điểm thâm nhập theo đường giá thực tế."

    def _a_echart_long_short_summary(self, trade_stats: Optional[Dict[str, Any]]) -> str:
        if not trade_stats:
            return "So sánh hiệu năng giữa hai chiều Long và Short."
        lw = trade_stats.get("long_win_rate", 0.0)
        sw = trade_stats.get("short_win_rate", 0.0)
        return f"Tỷ lệ thắng chiều Long đạt {lw}% so với chiều Short đạt {sw}%. Sự chênh lệch này cho thấy mức độ thích ứng của chiến lược theo xu hướng chủ đạo của tài sản."

    def _a_echart_mae_mfe_summary(self, trade_stats: Optional[Dict[str, Any]]) -> str:
        return "Phân tích mức độ gồng lỗ (MAE) và gồng lãi (MFE) giúp đánh giá xem lệnh có bị dính stop-loss quá sớm hoặc chốt lời quá muộn hay không."

    def _a_echart_account_margin_summary(self, k: Dict[str, Any]) -> str:
        return "Theo dõi số dư tài khoản thực tế và lượng ký quỹ khả dụng để quản lý rủi ro cháy tài sản và kiểm soát mức độ đòn bẩy."
