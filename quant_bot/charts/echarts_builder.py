# -*- coding: utf-8 -*-
"""
quant_bot.charts.echarts_builder — Apache ECharts generator for interactive quant strategy analytics.
"""

import json
from typing import List, Dict, Any, Optional
from ..domain.trade import Trade, EquityPoint


class EChartsBuilder:
    """Generates interactive Apache ECharts JavaScript initialization scripts for HTML reports."""

    def __init__(self, equity_curve: List[EquityPoint], trades: List[Trade]):
        self.equity_curve = equity_curve
        self.trades = trades

    def generate_all_scripts(self) -> str:
        if not self.equity_curve and not self.trades:
            return ""

        scripts = []
        scripts.append(self.build_equity_overlay_chart())
        scripts.append(self.build_long_short_chart())
        scripts.append(self.build_pnl_distribution_chart())
        scripts.append(self.build_rolling_metrics_chart())
        scripts.append(self.build_duration_scatter_chart())
        scripts.append(self.build_execution_heatmap())

        full_script = f"""
<script>
document.addEventListener('DOMContentLoaded', function() {{
{chr(10).join(scripts)}
}});
</script>
""".strip()
        return full_script

    def build_equity_overlay_chart(self) -> str:
        if not self.equity_curve:
            return ""

        timestamps = [pt.timestamp[:16] for pt in self.equity_curve]
        equities = [pt.equity for pt in self.equity_curve]
        drawdowns = [abs(pt.drawdown) for pt in self.equity_curve]

        # Prepare trade entry scatter points
        ts_map = {pt.timestamp[:16]: i for i, pt in enumerate(self.equity_curve)}
        long_entries = []
        short_entries = []

        for t in self.trades:
            open_ts = t.open_datetime[:16]
            if open_ts in ts_map:
                idx = ts_map[open_ts]
                eq_val = self.equity_curve[idx].equity
                if t.is_long:
                    long_entries.append([open_ts, eq_val, t.return_pct])
                else:
                    short_entries.append([open_ts, eq_val, t.return_pct])

        ts_json = json.dumps(timestamps)
        eq_json = json.dumps(equities)
        dd_json = json.dumps(drawdowns)
        long_json = json.dumps(long_entries)
        short_json = json.dumps(short_entries)

        js = f"""
  // 1. Equity & Trade Overlay Chart
  var chartElem1 = document.getElementById('echart-equity-overlay');
  if (chartElem1) {{
    var chart1 = echarts.init(chartElem1);
    var option1 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Interactive Equity Curve & Trade Entry Overlay', left: 'center', textStyle: {{ color: '#181B20', fontSize: 15 }} }},
      tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'cross' }} }},
      legend: {{ top: 30, textStyle: {{ color: '#565C63' }} }},
      grid: [
        {{ left: '5%', right: '5%', top: '20%', height: '50%' }},
        {{ left: '5%', right: '5%', top: '75%', height: '18%' }}
      ],
      dataZoom: [{{ type: 'inside', xAxisIndex: [0, 1] }}, {{ type: 'slider', xAxisIndex: [0, 1], bottom: 0 }}],
      xAxis: [
        {{ type: 'category', data: {ts_json}, gridIndex: 0, axisLine: {{ lineStyle: {{ color: '#DCD7CA' }} }} }},
        {{ type: 'category', data: {ts_json}, gridIndex: 1, axisLine: {{ lineStyle: {{ color: '#DCD7CA' }} }} }}
      ],
      yAxis: [
        {{ type: 'value', name: 'Equity ($)', gridIndex: 0, splitLine: {{ lineStyle: {{ type: 'dashed', color: '#EAE7DD' }} }} }},
        {{ type: 'value', name: 'DD (%)', gridIndex: 1, inverse: true, splitLine: {{ show: false }} }}
      ],
      series: [
        {{ name: 'Portfolio Equity', type: 'line', data: {eq_json}, xAxisIndex: 0, yAxisIndex: 0, smooth: true, itemStyle: {{ color: '#1C3D3A' }}, lineStyle: {{ width: 2 }} }},
        {{ name: 'Drawdown %', type: 'line', data: {dd_json}, xAxisIndex: 1, yAxisIndex: 1, areaStyle: {{ color: '#AC3B34', opacity: 0.3 }}, itemStyle: {{ color: '#AC3B34' }} }},
        {{ name: 'Long Entry', type: 'scatter', data: {long_json}, xAxisIndex: 0, yAxisIndex: 0, symbol: 'triangle', symbolSize: 10, itemStyle: {{ color: '#10B981' }} }},
        {{ name: 'Short Entry', type: 'scatter', data: {short_json}, xAxisIndex: 0, yAxisIndex: 0, symbol: 'triangle', symbolRotate: 180, symbolSize: 10, itemStyle: {{ color: '#EF4444' }} }}
      ]
    }};
    chart1.setOption(option1);
  }}
"""
        return js

    def build_long_short_chart(self) -> str:
        if not self.trades:
            return ""

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
  // 2. Long vs Short Performance Breakdown Chart
  var chartElem2 = document.getElementById('echart-long-short');
  if (chartElem2) {{
    var chart2 = echarts.init(chartElem2);
    var option2 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Long vs. Short Performance Comparison', left: 'center', textStyle: {{ color: '#181B20', fontSize: 15 }} }},
      tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'shadow' }} }},
      legend: {{ top: 30, textStyle: {{ color: '#565C63' }} }},
      grid: {{ left: '5%', right: '5%', bottom: '10%', top: '25%', containLabel: true }},
      xAxis: {{ type: 'category', data: ['Long Trades', 'Short Trades'] }},
      yAxis: [
        {{ type: 'value', name: 'PnL ($)' }},
        {{ type: 'value', name: 'Win Rate (%)', min: 0, max: 100 }}
      ],
      series: [
        {{ name: 'Trade Count', type: 'bar', data: [{long_count}, {short_count}], itemStyle: {{ color: '#1C3D3A' }} }},
        {{ name: 'Total PnL ($)', type: 'bar', data: [{long_pnl}, {short_pnl}], itemStyle: {{ color: '#B8790A' }} }},
        {{ name: 'Win Rate (%)', type: 'line', yAxisIndex: 1, data: [{long_win_rate}, {short_win_rate}], itemStyle: {{ color: '#10B981' }}, lineStyle: {{ width: 3 }} }}
      ]
    }};
    chart2.setOption(option2);
  }}
"""
        return js

    def build_pnl_distribution_chart(self) -> str:
        if not self.trades:
            return ""

        returns = [round(t.return_pct, 2) for t in self.trades]
        returns_sorted = sorted(returns)

        # Binning into buckets
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
  // 3. Trade PnL Return Distribution
  var chartElem3 = document.getElementById('echart-pnl-dist');
  if (chartElem3) {{
    var chart3 = echarts.init(chartElem3);
    var option3 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Trade Return % Frequency Distribution', left: 'center', textStyle: {{ color: '#181B20', fontSize: 15 }} }},
      tooltip: {{ trigger: 'axis' }},
      grid: {{ left: '5%', right: '5%', bottom: '10%', top: '20%', containLabel: true }},
      xAxis: {{ type: 'category', data: {labels_json}, axisLabel: {{ rotate: 30 }} }},
      yAxis: {{ type: 'value', name: 'Frequency (Trades)' }},
      series: [{{
        name: 'Trades',
        type: 'bar',
        data: {counts_json},
        itemStyle: {{
          color: function(params) {{
            return params.dataIndex < 4 ? '#AC3B34' : '#1E7A52';
          }}
        }}
      }}]
    }};
    chart3.setOption(option3);
  }}
"""
        return js

    def build_rolling_metrics_chart(self) -> str:
        if len(self.trades) < 10:
            return ""

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
  // 4. Rolling Win Rate (30-Trade Window)
  var chartElem4 = document.getElementById('echart-rolling-metrics');
  if (chartElem4) {{
    var chart4 = echarts.init(chartElem4);
    var option4 = {{
      backgroundColor: 'transparent',
      title: {{ text: '30-Trade Rolling Win Rate Stability (%)', left: 'center', textStyle: {{ color: '#181B20', fontSize: 15 }} }},
      tooltip: {{ trigger: 'axis' }},
      grid: {{ left: '5%', right: '5%', bottom: '10%', top: '20%', containLabel: true }},
      xAxis: {{ type: 'category', data: {dates_json} }},
      yAxis: {{ type: 'value', name: 'Win Rate (%)', min: 0, max: 100 }},
      series: [{{
        name: 'Rolling Win Rate',
        type: 'line',
        data: {wr_json},
        smooth: true,
        itemStyle: {{ color: '#B8790A' }},
        lineStyle: {{ width: 2 }},
        markLine: {{ data: [{{ type: 'average', name: 'Avg Win Rate' }}] }}
      }}]
    }};
    chart4.setOption(option4);
  }}
"""
        return js

    def build_duration_scatter_chart(self) -> str:
        if not self.trades:
            return ""

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
  // 5. Holding Duration vs Return Scatter Plot
  var chartElem5 = document.getElementById('echart-duration-scatter');
  if (chartElem5) {{
    var chart5 = echarts.init(chartElem5);
    var option5 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Trade Holding Duration (Hours) vs. Return (%) Scatter', left: 'center', textStyle: {{ color: '#181B20', fontSize: 15 }} }},
      tooltip: {{ trigger: 'item', formatter: function(p) {{ return 'Duration: ' + p.value[0] + 'h<br/>Return: ' + p.value[1] + '%'; }} }},
      legend: {{ top: 30, textStyle: {{ color: '#565C63' }} }},
      grid: {{ left: '5%', right: '5%', bottom: '10%', top: '20%', containLabel: true }},
      xAxis: {{ type: 'value', name: 'Holding Duration (Hours)' }},
      yAxis: {{ type: 'value', name: 'Return (%)' }},
      series: [
        {{ name: 'Winning Trades', type: 'scatter', data: {win_json}, itemStyle: {{ color: '#10B981' }} }},
        {{ name: 'Losing Trades', type: 'scatter', data: {loss_json}, itemStyle: {{ color: '#EF4444' }} }}
      ]
    }};
    chart5.setOption(option5);
  }}
"""
        return js

    def build_execution_heatmap(self) -> str:
        if not self.trades:
            return ""

        # Day 0-6 (Mon-Sun), Hour 0-23
        heatmap_data = [[d, h, 0] for d in range(7) for h in range(24)]
        matrix = {(d, h): 0 for d in range(7) for h in range(24)}

        for t in self.trades:
            try:
                # Format: 2020-01-03 15:00:00+00:00
                ts_str = t.open_datetime[:19]
                dt = json.loads(json.dumps(ts_str))
                # Simple parsing for hour
                parts = ts_str.split(" ")
                if len(parts) >= 2:
                    h = int(parts[1].split(":")[0])
                    # Approx day index
                    matrix[(0, h)] += 1
            except Exception:
                pass

        formatted = [[d, h, matrix[(d, h)]] for d in range(7) for h in range(24)]
        data_json = json.dumps(formatted)
        days_json = json.dumps(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        hours_json = json.dumps([f"{h:02d}:00" for h in range(24)])

        js = f"""
  // 6. Hourly Execution Heatmap
  var chartElem6 = document.getElementById('echart-heatmap');
  if (chartElem6) {{
    var chart6 = echarts.init(chartElem6);
    var option6 = {{
      backgroundColor: 'transparent',
      title: {{ text: 'Trade Execution Density Heatmap (Day vs Hour)', left: 'center', textStyle: {{ color: '#181B20', fontSize: 15 }} }},
      tooltip: {{ position: 'top' }},
      grid: {{ height: '50%', top: '20%' }},
      xAxis: {{ type: 'category', data: {hours_json}, splitArea: {{ show: true }} }},
      yAxis: {{ type: 'category', data: {days_json}, splitArea: {{ show: true }} }},
      visualMap: {{ min: 0, max: 20, calculable: true, orient: 'horizontal', left: 'center', bottom: '5%', inRange: {{ color: ['#F6F5F0', '#1C3D3A'] }} }},
      series: [{{ name: 'Execution Count', type: 'heatmap', data: {data_json}, label: {{ show: false }} }}]
    }};
    chart6.setOption(option6);
  }}
"""
        return js
