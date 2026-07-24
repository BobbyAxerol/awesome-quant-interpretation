# -*- coding: utf-8 -*-
"""
quant_bot.charts.echarts_builder — Apache ECharts generator for interactive quant strategy analytics.
Generates TradingView/QuantConnect-style insight charts with clean grid padding, legends, and tooltips.
"""

import json
from typing import List, Dict, Any, Optional
from ..domain.trade import Trade, EquityPoint


class EChartsBuilder:
    """Generates interactive Apache ECharts JavaScript initialization scripts for HTML reports."""

    def __init__(
        self,
        equity_curve: List[EquityPoint],
        trades: List[Trade],
        account_history: Optional[List[Dict[str, Any]]] = None,
        prefix: str = "train-",
    ):
        self.equity_curve = equity_curve
        self.trades = trades
        self.account_history = account_history or []
        self.prefix = prefix

    def generate_all_scripts(self) -> str:
        if not self.equity_curve and not self.trades:
            return ""

        scripts = [
            self.build_standalone_equity_chart(),
            self.build_price_trade_signals_chart(),
            self.build_long_short_chart(),
            self.build_mae_mfe_scatter_chart(),
            self.build_account_margin_chart(),
            self.build_pnl_distribution_chart(),
            self.build_rolling_metrics_chart(),
            self.build_duration_scatter_chart(),
            self.build_execution_heatmap(),
        ]

        valid_scripts = [s for s in scripts if s.strip()]

        full_script = f"""
<script>
document.addEventListener('DOMContentLoaded', function() {{
{chr(10).join(valid_scripts)}
}});
</script>
""".strip()
        return full_script

    def build_standalone_equity_chart(self) -> str:
        if not self.equity_curve:
            return ""

        elem_id = f"{self.prefix}echart-equity-waterfall"
        timestamps = [pt.timestamp[:16] for pt in self.equity_curve]
        equities = [pt.equity for pt in self.equity_curve]
        drawdowns = [abs(pt.drawdown) for pt in self.equity_curve]

        ts_json = json.dumps(timestamps)
        eq_json = json.dumps(equities)
        dd_json = json.dumps(drawdowns)

        js = f"""
  // Standalone Equity & Drawdown Waterfall
  var elem1 = document.getElementById('{elem_id}');
  if (elem1) {{
    var chart1 = echarts.init(elem1);
    var option1 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Standalone Equity Curve & Drawdown Waterfall', left: 'center', textStyle: {{ color: '#181B20', fontSize: 14, fontWeight: 'bold' }} }},
      tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'cross' }} }},
      legend: {{ top: 28, textStyle: {{ color: '#565C63', fontSize: 11 }} }},
      grid: [
        {{ left: '6%', right: '5%', top: '22%', height: '48%', containLabel: true }},
        {{ left: '6%', right: '5%', top: '74%', height: '18%', containLabel: true }}
      ],
      dataZoom: [{{ type: 'inside', xAxisIndex: [0, 1] }}, {{ type: 'slider', xAxisIndex: [0, 1], bottom: 2, height: 18 }}],
      xAxis: [
        {{ type: 'category', data: {ts_json}, gridIndex: 0, axisLine: {{ lineStyle: {{ color: '#DCD7CA' }} }}, axisLabel: {{ color: '#565C63', fontSize: 10 }} }},
        {{ type: 'category', data: {ts_json}, gridIndex: 1, axisLine: {{ lineStyle: {{ color: '#DCD7CA' }} }}, axisLabel: {{ color: '#565C63', fontSize: 10 }} }}
      ],
      yAxis: [
        {{ type: 'value', name: 'Portfolio Equity ($)', gridIndex: 0, splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }}, axisLabel: {{ color: '#565C63', fontSize: 10 }} }},
        {{ type: 'value', name: 'Drawdown (%)', gridIndex: 1, inverse: true, splitLine: {{ show: false }}, axisLabel: {{ color: '#565C63', fontSize: 10 }} }}
      ],
      series: [
        {{ name: 'Equity ($)', type: 'line', data: {eq_json}, xAxisIndex: 0, yAxisIndex: 0, smooth: true, itemStyle: {{ color: '#1C3D3A' }}, lineStyle: {{ width: 2 }} }},
        {{ name: 'Drawdown (%)', type: 'line', data: {dd_json}, xAxisIndex: 1, yAxisIndex: 1, areaStyle: {{ color: '#AC3B34', opacity: 0.35 }}, itemStyle: {{ color: '#AC3B34' }} }}
      ]
    }};
    chart1.setOption(option1);
  }}
"""
        return js

    def build_price_trade_signals_chart(self) -> str:
        if not self.trades:
            return ""

        elem_id = f"{self.prefix}echart-price-signals"
        buy_signals = []
        sell_signals = []

        for t in self.trades:
            open_ts = t.open_datetime[:16]
            if t.is_long:
                buy_signals.append([open_ts, t.entry_price, t.realized_pnl])
            else:
                sell_signals.append([open_ts, t.entry_price, t.realized_pnl])

        buy_json = json.dumps(buy_signals)
        sell_json = json.dumps(sell_signals)

        js = f"""
  // Price Action & Trade Signals Overlay
  var elem2 = document.getElementById('{elem_id}');
  if (elem2) {{
    var chart2 = echarts.init(elem2);
    var option2 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Market Price Action & Execution Signals (Buy/Sell Price Mapping)', left: 'center', textStyle: {{ color: '#181B20', fontSize: 14, fontWeight: 'bold' }} }},
      tooltip: {{ trigger: 'item', formatter: function(p) {{ return 'Time: ' + p.value[0] + '<br/>Entry Price: $' + p.value[1] + '<br/>PnL: $' + p.value[2]; }} }},
      legend: {{ top: 28, textStyle: {{ color: '#565C63', fontSize: 11 }} }},
      grid: {{ left: '6%', right: '5%', top: '22%', bottom: '15%', containLabel: true }},
      xAxis: {{ type: 'category', axisLine: {{ lineStyle: {{ color: '#DCD7CA' }} }}, axisLabel: {{ color: '#565C63', fontSize: 10 }} }},
      yAxis: {{ type: 'value', name: 'Execution Price ($)', splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }}, axisLabel: {{ color: '#565C63', fontSize: 10 }} }},
      series: [
        {{ name: 'Long Entry (Buy)', type: 'scatter', data: {buy_json}, symbol: 'triangle', symbolSize: 10, itemStyle: {{ color: '#10B981' }} }},
        {{ name: 'Short Entry (Sell)', type: 'scatter', data: {sell_json}, symbol: 'triangle', symbolRotate: 180, symbolSize: 10, itemStyle: {{ color: '#EF4444' }} }}
      ]
    }};
    chart2.setOption(option2);
  }}
"""
        return js

    def build_long_short_chart(self) -> str:
        if not self.trades:
            return ""

        elem_id = f"{self.prefix}echart-long-short"
        long_trades = [t for t in self.trades if t.is_long]
        short_trades = [t for t in self.trades if not t.is_long]

        long_count = len(long_trades)
        short_count = len(short_trades)
        long_wins = sum(1 for t in long_trades if t.is_win)
        short_wins = sum(1 for t in short_trades if t.is_win)

        long_win_rate = round((long_wins / long_count) * 100.0, 2) if long_count > 0 else 0.0
        short_win_rate = round((short_wins / short_count) * 100.0, 2) if short_count > 0 else 0.0

        long_pnl = round(sum(t.realized_pnl for t in long_trades), 2)
        short_pnl = round(sum(t.realized_pnl for t in short_trades), 2)

        js = f"""
  // Long vs Short Performance Breakdown
  var elem3 = document.getElementById('{elem_id}');
  if (elem3) {{
    var chart3 = echarts.init(elem3);
    var option3 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Long vs. Short Performance Breakdown', left: 'center', textStyle: {{ color: '#181B20', fontSize: 14, fontWeight: 'bold' }} }},
      tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }} }},
      legend: {{ top: 28, textStyle: {{ color: '#565C63', fontSize: 11 }} }},
      grid: {{ left: '6%', right: '6%', top: '24%', bottom: '12%', containLabel: true }},
      xAxis: {{ type: 'category', data: ['Long Trades', 'Short Trades'], axisLabel: {{ color: '#565C63', fontSize: 11 }} }},
      yAxis: [
        {{ type: 'value', name: 'PnL ($)', splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }} }},
        {{ type: 'value', name: 'Win Rate (%)', min: 0, max: 100 }}
      ],
      series: [
        {{ name: 'Trade Count', type: 'bar', data: [{long_count}, {short_count}], itemStyle: {{ color: '#1C3D3A' }} }},
        {{ name: 'Total PnL ($)', type: 'bar', data: [{long_pnl}, {short_pnl}], itemStyle: {{ color: '#B8790A' }} }},
        {{ name: 'Win Rate (%)', type: 'line', yAxisIndex: 1, data: [{long_win_rate}, {short_win_rate}], itemStyle: {{ color: '#10B981' }}, lineStyle: {{ width: 3 }} }}
      ]
    }};
    chart3.setOption(option3);
  }}
"""
        return js

    def build_mae_mfe_scatter_chart(self) -> str:
        if not self.trades:
            return ""

        elem_id = f"{self.prefix}echart-mae-mfe"
        scatter_data = []

        for t in self.trades:
            # Approximate Adverse vs Favorable Excursion from return_pct and fee ratio
            mae = abs(min(0.0, t.return_pct * 0.4))
            mfe = max(0.0, t.return_pct)
            scatter_data.append([round(mae, 2), round(mfe, 2), round(t.realized_pnl, 2)])

        data_json = json.dumps(scatter_data)

        js = f"""
  // MAE / MFE Excursion Distribution
  var elem4 = document.getElementById('{elem_id}');
  if (elem4) {{
    var chart4 = echarts.init(elem4);
    var option4 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Maximum Adverse (MAE) vs Favorable (MFE) Excursion', left: 'center', textStyle: {{ color: '#181B20', fontSize: 14, fontWeight: 'bold' }} }},
      tooltip: {{ trigger: 'item', formatter: function(p) {{ return 'MAE: ' + p.value[0] + '%<br/>MFE: ' + p.value[1] + '%<br/>PnL: $' + p.value[2]; }} }},
      legend: {{ top: 28, textStyle: {{ color: '#565C63', fontSize: 11 }} }},
      grid: {{ left: '6%', right: '6%', top: '22%', bottom: '12%', containLabel: true }},
      xAxis: {{ type: 'value', name: 'MAE (%)', splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }} }},
      yAxis: {{ type: 'value', name: 'MFE (%)', splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }} }},
      series: [{{
        name: 'Trade Distribution',
        type: 'scatter',
        data: {data_json},
        itemStyle: {{
          color: function(p) {{ return p.value[2] >= 0 ? '#10B981' : '#EF4444'; }}
        }}
      }}]
    }};
    chart4.setOption(option4);
  }}
"""
        return js

    def build_account_margin_chart(self) -> str:
        elem_id = f"{self.prefix}echart-account-margin"
        if not self.account_history:
            return ""

        timestamps = [a.get("timestamp", "")[:16] for a in self.account_history[:200]]
        totals = [float(a.get("total", 0.0)) for a in self.account_history[:200]]
        frees = [float(a.get("free", 0.0)) for a in self.account_history[:200]]

        ts_json = json.dumps(timestamps)
        tot_json = json.dumps(totals)
        free_json = json.dumps(frees)

        js = f"""
  // Account Balance & Free Margin Utilization
  var elem5 = document.getElementById('{elem_id}');
  if (elem5) {{
    var chart5 = echarts.init(elem5);
    var option5 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Account Total Equity vs. Free Margin ($)', left: 'center', textStyle: {{ color: '#181B20', fontSize: 14, fontWeight: 'bold' }} }},
      tooltip: {{ trigger: 'axis' }},
      legend: {{ top: 28, textStyle: {{ color: '#565C63', fontSize: 11 }} }},
      grid: {{ left: '6%', right: '5%', top: '22%', bottom: '12%', containLabel: true }},
      xAxis: {{ type: 'category', data: {ts_json}, axisLabel: {{ color: '#565C63', fontSize: 10 }} }},
      yAxis: {{ type: 'value', name: 'Amount ($)', splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }} }},
      series: [
        {{ name: 'Total Equity ($)', type: 'line', data: {tot_json}, itemStyle: {{ color: '#1C3D3A' }}, lineStyle: {{ width: 2 }} }},
        {{ name: 'Free Margin ($)', type: 'line', data: {free_json}, itemStyle: {{ color: '#B8790A' }}, lineStyle: {{ width: 1.5, type: 'dashed' }} }}
      ]
    }};
    chart5.setOption(option5);
  }}
"""
        return js

    def build_pnl_distribution_chart(self) -> str:
        if not self.trades:
            return ""

        elem_id = f"{self.prefix}echart-pnl-dist"
        returns = [round(t.return_pct, 2) for t in self.trades]

        bins = [-10, -5, -3, -1, 0, 1, 3, 5, 10, 20, 50]
        bin_counts = [0] * (len(bins) - 1)
        bin_labels = [f"{bins[i]}% to {bins[i+1]}%" for i in range(len(bins) - 1)]

        for r in returns:
            for i in range(len(bins) - 1):
                if bins[i] <= r < bins[i+1]:
                    bin_counts[i] += 1
                    break

        labels_json = json.dumps(bin_labels)
        counts_json = json.dumps(bin_counts)

        js = f"""
  // Trade PnL Return Frequency
  var elem6 = document.getElementById('{elem_id}');
  if (elem6) {{
    var chart6 = echarts.init(elem6);
    var option6 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Trade Return % Frequency Distribution', left: 'center', textStyle: {{ color: '#181B20', fontSize: 14, fontWeight: 'bold' }} }},
      tooltip: {{ trigger: 'axis' }},
      grid: {{ left: '6%', right: '5%', top: '22%', bottom: '18%', containLabel: true }},
      xAxis: {{ type: 'category', data: {labels_json}, axisLabel: {{ rotate: 30, color: '#565C63', fontSize: 10 }} }},
      yAxis: {{ type: 'value', name: 'Frequency (Trades)', splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }} }},
      series: [{{
        name: 'Trades',
        type: 'bar',
        data: {counts_json},
        itemStyle: {{
          color: function(params) {{ return params.dataIndex < 4 ? '#AC3B34' : '#1E7A52'; }}
        }}
      }}]
    }};
    chart6.setOption(option6);
  }}
"""
        return js

    def build_rolling_metrics_chart(self) -> str:
        if len(self.trades) < 10:
            return ""

        elem_id = f"{self.prefix}echart-rolling-metrics"
        window = 30
        dates = []
        rolling_win_rates = []

        for i in range(window, len(self.trades)):
            sub = self.trades[i - window : i]
            wins = sum(1 for t in sub if t.is_win)
            wr = round((wins / window) * 100.0, 2)
            dates.append(sub[-1].close_datetime[:10])
            rolling_win_rates.append(wr)

        dates_json = json.dumps(dates)
        wr_json = json.dumps(rolling_win_rates)

        js = f"""
  // 30-Trade Rolling Win Rate Stability
  var elem7 = document.getElementById('{elem_id}');
  if (elem7) {{
    var chart7 = echarts.init(elem7);
    var option7 = {{
      backgroundColor: 'transparent',
      title: {{ text: '30-Trade Rolling Win Rate Stability (%)', left: 'center', textStyle: {{ color: '#181B20', fontSize: 14, fontWeight: 'bold' }} }},
      tooltip: {{ trigger: 'axis' }},
      grid: {{ left: '6%', right: '5%', top: '22%', bottom: '12%', containLabel: true }},
      xAxis: {{ type: 'category', data: {dates_json}, axisLabel: {{ color: '#565C63', fontSize: 10 }} }},
      yAxis: {{ type: 'value', name: 'Win Rate (%)', min: 0, max: 100, splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }} }},
      series: [{{
        name: 'Rolling Win Rate',
        type: 'line',
        data: {wr_json},
        smooth: true,
        itemStyle: {{ color: '#B8790A' }},
        lineStyle: {{ width: 2 }}
      }}]
    }};
    chart7.setOption(option7);
  }}
"""
        return js

    def build_duration_scatter_chart(self) -> str:
        if not self.trades:
            return ""

        elem_id = f"{self.prefix}echart-duration-scatter"
        win_data = []
        loss_data = []

        for t in self.trades:
            pt = [round(t.duration_hours, 2), round(t.return_pct, 2)]
            if t.is_win:
                win_data.append(pt)
            else:
                loss_data.append(pt)

        win_json = json.dumps(win_data)
        loss_json = json.dumps(loss_data)

        js = f"""
  // Holding Duration vs Return Scatter
  var elem8 = document.getElementById('{elem_id}');
  if (elem8) {{
    var chart8 = echarts.init(elem8);
    var option8 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Trade Holding Duration (Hours) vs. Return (%) Scatter', left: 'center', textStyle: {{ color: '#181B20', fontSize: 14, fontWeight: 'bold' }} }},
      tooltip: {{ trigger: 'item', formatter: function(p) {{ return 'Duration: ' + p.value[0] + 'h<br/>Return: ' + p.value[1] + '%'; }} }},
      legend: {{ top: 28, textStyle: {{ color: '#565C63', fontSize: 11 }} }},
      grid: {{ left: '6%', right: '5%', top: '22%', bottom: '12%', containLabel: true }},
      xAxis: {{ type: 'value', name: 'Holding Duration (Hours)', splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }} }},
      yAxis: {{ type: 'value', name: 'Return (%)', splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }} }},
      series: [
        {{ name: 'Winning Trades', type: 'scatter', data: {win_json}, itemStyle: {{ color: '#10B981' }} }},
        {{ name: 'Losing Trades', type: 'scatter', data: {loss_json}, itemStyle: {{ color: '#EF4444' }} }}
      ]
    }};
    chart8.setOption(option8);
  }}
"""
        return js

    def build_execution_heatmap(self) -> str:
        if not self.trades:
            return ""

        elem_id = f"{self.prefix}echart-heatmap"
        matrix = {(d, h): 0 for d in range(7) for h in range(24)}

        for t in self.trades:
            try:
                ts_str = t.open_datetime[:19]
                parts = ts_str.split(" ")
                if len(parts) >= 2:
                    h = int(parts[1].split(":")[0])
                    matrix[(0, h)] += 1
            except Exception:
                pass

        formatted = [[d, h, matrix[(d, h)]] for d in range(7) for h in range(24)]
        data_json = json.dumps(formatted)
        days_json = json.dumps(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        hours_json = json.dumps([f"{h:02d}:00" for h in range(24)])

        js = f"""
  // Hourly Execution Heatmap
  var elem9 = document.getElementById('{elem_id}');
  if (elem9) {{
    var chart9 = echarts.init(elem9);
    var option9 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Trade Execution Density Heatmap (Day vs Hour)', left: 'center', textStyle: {{ color: '#181B20', fontSize: 14, fontWeight: 'bold' }} }},
      tooltip: {{ position: 'top' }},
      grid: {{ height: '48%', top: '22%', left: '6%', right: '5%', containLabel: true }},
      xAxis: {{ type: 'category', data: {hours_json}, splitArea: {{ show: true }}, axisLabel: {{ fontSize: 9 }} }},
      yAxis: {{ type: 'category', data: {days_json}, splitArea: {{ show: true }}, axisLabel: {{ fontSize: 10 }} }},
      visualMap: {{ min: 0, max: 20, calculable: true, orient: 'horizontal', left: 'center', bottom: '2%', inRange: {{ color: ['#F6F5F0', '#1C3D3A'] }} }},
      series: [{{ name: 'Execution Count', type: 'heatmap', data: {data_json}, label: {{ show: false }} }}]
    }};
    chart9.setOption(option9);
  }}
"""
        return js
