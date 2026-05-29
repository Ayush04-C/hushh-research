"""
Agent Kai — Macro-Economic Agent (ADK Compliant)

Analyzes macroeconomic factors, inflation, interest rates, and sector trends.
Extended from HushhAgent for consent enforcement.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from hushh_mcp.agents.base_agent import HushhAgent
from hushh_mcp.constants import GEMINI_MODEL, KAI_LLM_MAX_OUTPUT_TOKENS_DEFAULT
from hushh_mcp.operons.kai.llm import (
    _generate_content_text,
    is_gemini_ready,
)

logger = logging.getLogger(__name__)


@dataclass
class MacroInsight:
    """Macro-economic analysis insight with sources and confidence."""

    summary: str
    interest_rate_impact: str
    inflation_impact: str
    sector_trend: str
    macro_bull_case: str
    macro_bear_case: str
    confidence: float
    recommendation: str  # "buy", "hold", "reduce"
    sources: List[str]


class MacroAgent(HushhAgent):
    """
    Macro Agent - Analyzes broader economic factors impacting the asset.
    """

    def __init__(self, processing_mode: str = "hybrid"):
        self.agent_id = "macro"
        self.processing_mode = processing_mode
        self.color = "#f59e0b"  # Amber
        self.system_prompt = """
            You are a Macro-Economic Analyst focused on interest rates, inflation, and sector trends.
            Your job is to analyze how broader economic conditions will impact a specific company's performance.
            """

        super().__init__(
            name="Macro-Economic Agent",
            model=GEMINI_MODEL,
            system_prompt=self.system_prompt,
            required_scopes=["agent.kai.macro"],
        )

    async def analyze(
        self,
        ticker: str,
        user_id: str,
        consent_token: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> MacroInsight:
        """
        Perform macro-economic analysis.
        """
        logger.info(f"[Macro] Orchestrating macro analysis for {ticker}")

        if not is_gemini_ready() or self.processing_mode != "hybrid":
            return self._build_deterministic_fallback(
                ticker, "Gemini LLM unavailable or offline mode."
            )

        try:
            # We will use Gemini to generate a macro outlook based on general market context.
            # In a full implementation, we would fetch live Fed rates, CPI data, etc.
            prompt = f"{self.system_prompt}\n\n" + f"""
            Analyze the macro-economic outlook for {ticker}.
            Consider current high-level market trends, interest rate environments, and inflation.
            
            Return ONLY a valid JSON object with EXACTLY these keys:
            {{
                "summary": "2 sentence summary of macro impact on this stock",
                "interest_rate_impact": "How current rates affect this business",
                "inflation_impact": "How inflation affects their costs/pricing",
                "sector_trend": "Overall trend for their industry",
                "macro_bull_case": "Macro tailwinds",
                "macro_bear_case": "Macro headwinds",
                "recommendation": "buy, hold, or reduce based solely on macro",
                "confidence": 0.85
            }}
            """

            import asyncio
            import json

            json_str = ""
            for attempt in range(2):
                try:
                    json_str = await _generate_content_text(
                        prompt=prompt,
                        timeout_seconds=45.0,
                        max_output_tokens=KAI_LLM_MAX_OUTPUT_TOKENS_DEFAULT,
                        response_mime_type="application/json",
                    )
                    break
                except Exception as e:
                    logger.warning(
                        f"[Macro] Gemini analysis failed (attempt {attempt + 1}/2): {e}"
                    )
                    if attempt == 1:
                        raise
                    await asyncio.sleep(2.0)

            if not json_str:
                raise ValueError("Empty response received from LLM")

            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()

            analysis = json.loads(json_str)

            return MacroInsight(
                summary=analysis.get("summary", "Macro analysis completed."),
                interest_rate_impact=analysis.get("interest_rate_impact", "Neutral"),
                inflation_impact=analysis.get("inflation_impact", "Neutral"),
                sector_trend=analysis.get("sector_trend", "Neutral"),
                macro_bull_case=analysis.get("macro_bull_case", "Favorable economic conditions."),
                macro_bear_case=analysis.get("macro_bear_case", "Economic headwinds."),
                confidence=float(analysis.get("confidence", 0.70)),
                recommendation=analysis.get("recommendation", "hold").lower(),
                sources=["Gemini Macro-Economic Model"],
            )

        except Exception as e:
            logger.error(f"[Macro] Error during analysis: {e}")
            return self._build_deterministic_fallback(ticker, str(e))

    def _build_deterministic_fallback(self, ticker: str, reason: str) -> MacroInsight:
        return MacroInsight(
            summary=f"Deterministic macro analysis for {ticker}. {reason}",
            interest_rate_impact="Unknown due to missing data.",
            inflation_impact="Unknown due to missing data.",
            sector_trend="Market-wide correlation assumed.",
            macro_bull_case="Broad market recovery lifts all assets.",
            macro_bear_case="Systemic shock risks.",
            confidence=0.40,
            recommendation="hold",
            sources=["Deterministic Fallback"],
        )


macro_agent = MacroAgent()
