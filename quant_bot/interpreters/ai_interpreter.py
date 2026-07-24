# -*- coding: utf-8 -*-
"""
quant_bot.interpreters.ai_interpreter — Free AI Model API Strategy Interpretation Engine.
Supports Google Gemini Free API Tier & Groq API with zero-dependency urllib HTTP fallback.
"""

import json
import os
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional
from ..domain.trade import Trade
from ..domain.metrics import BadgeStatus
from .base import BaseInterpreter
from .rule_interpreter import RuleBasedStrategyInterpreter


class AIStrategyInterpreter(BaseInterpreter):
    """AI / LLM-powered Strategy Interpretation engine with fallback to Rule-based engine."""

    def __init__(self, api_key: Optional[str] = None, provider: str = "gemini"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GROQ_API_KEY")
        self.provider = provider.lower()
        self.fallback_interpreter = RuleBasedStrategyInterpreter()

    def generate_analysis(
        self,
        kpi: Dict[str, Any],
        eoy: List[Dict[str, Any]],
        drawdowns: List[Dict[str, Any]],
        badges: Dict[str, BadgeStatus],
        trades: List[Trade] = None,
        trade_stats: Dict[str, Any] = None,
    ) -> Dict[str, str]:
        # Always generate baseline rule-based analysis
        analysis = self.fallback_interpreter.generate_analysis(
            kpi=kpi, eoy=eoy, drawdowns=drawdowns, badges=badges, trades=trades, trade_stats=trade_stats
        )

        if not self.api_key:
            return analysis

        # Call AI API for qualitative stakeholder summary if key is set
        try:
            ai_summary = self._call_ai_api(kpi, badges, trade_stats)
            if ai_summary:
                analysis["ai_executive_interpretation"] = ai_summary
        except Exception as e:
            print(f"[!] AI API call warning (using fallback): {e}")

        return analysis

    def _call_ai_api(self, kpi: Dict[str, Any], badges: Dict[str, BadgeStatus], trade_stats: Optional[Dict[str, Any]]) -> Optional[str]:
        prompt_data = {
            "cagr": kpi.get("cagrpct"),
            "max_drawdown": kpi.get("max_drawdown"),
            "profit_factor": kpi.get("profit_factor"),
            "sharpe": kpi.get("sharpe"),
            "trade_stats": trade_stats,
        }

        prompt_text = (
            "Bạn là một Quantitative Analyst chuyên nghiệp. Dựa trên số liệu chiến lược định lượng sau, "
            "hãy viết 1 đoạn nhận định chuyên sâu bằng tiếng Việt (2-3 câu) dành cho nhà đầu tư/stakeholder:\n"
            f"{json.dumps(prompt_data, ensure_ascii=False, indent=2)}\n"
        )

        if "groq" in self.provider or self.api_key.startswith("gsk_"):
            return self._call_groq(prompt_text)
        else:
            return self._call_gemini(prompt_text)

    def _call_gemini(self, prompt: str) -> Optional[str]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            candidates = res_json.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "").strip()
        return None

    def _call_groq(self, prompt: str) -> Optional[str]:
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            choices = res_json.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "").strip()
        return None
