"""
Agent Kai — Macro-Economic Agent (ADK Compliant)

Analyzes macroeconomic factors, inflation, interest rates, and sector trends.
Extended from HushhAgent for consent enforcement.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from hushh_mcp.agents.base_agent import HushhAgent
from hushh_mcp.constants import GEMINI_MODEL

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

        # Initialize with proper ADK parameters
        super().__init__(
            name="Macro-Economic Agent",
            model=GEMINI_MODEL,  # Standardized model
            system_prompt="""
            You are a Macro-Economic Analyst focused on interest rates, inflation, and sector trends.
            Your job is to analyze how broader economic conditions will impact a specific company's performance.
            """,
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
        Perform macro-economic analysis using Gemini + operons.
        """
        if not consent_token:
            raise PermissionError("Macro analysis requires a consent token")

        logger.info(f"[Macro] Orchestrating analysis for {ticker} - user {user_id}")

        # Operon 1: Fetch market data for baseline context
        from hushh_mcp.operons.kai.fetchers import fetch_macro_indicators, fetch_market_data

        market_data: Optional[Dict[str, Any]] = None
        try:
            market_data = await fetch_market_data(ticker, user_id, consent_token)
        except Exception as e:
            logger.warning(f"[Macro] Market snapshot unavailable for {ticker}: {e}")
            market_data = {}

        # Operon 1b: Fetch live macro indicators (VIX, 10-Year Treasury yield).
        # Graceful degradation: a failed fetch falls back to defaults inside the operon;
        # the analysis pipeline must never hard-block on supplemental macro data.
        macro_indicators: Dict[str, Any] = {}
        try:
            macro_indicators = await fetch_macro_indicators(user_id, consent_token)
            logger.info(
                "[Macro] Live indicators fetched — VIX=%.2f, 10Y=%.2f%%",
                macro_indicators.get("vix", 0),
                macro_indicators.get("treasury_yield_10y", 0),
            )
        except Exception as e:
            logger.warning(
                "[Macro] Live macro indicators unavailable for %s, using defaults: %s",
                ticker,
                e,
            )

        # Operon 2: Gemini Deep Macro Analysis
        from hushh_mcp.operons.kai.llm import (
            analyze_macro_with_gemini,
            get_gemini_unavailable_reason,
            is_gemini_ready,
        )

        gemini_analysis = None
        if self.processing_mode == "hybrid" and consent_token:
            if not is_gemini_ready():
                logger.warning(
                    "[Macro] Gemini unavailable, using deterministic analysis: %s",
                    get_gemini_unavailable_reason(),
                )
            for attempt in range(2):
                try:
                    gemini_analysis = await analyze_macro_with_gemini(
                        ticker=ticker,
                        user_id=user_id,
                        consent_token=consent_token,
                        market_data=market_data,
                        macro_indicators=macro_indicators,
                        user_context=context,
                    )
                    break
                except Exception as e:
                    logger.warning(
                        f"[Macro] Gemini analysis failed (attempt {attempt + 1}/2): {e}"
                    )
                    if attempt == 1:
                        logger.warning(
                            "[Macro] Max retries reached. Falling back to deterministic."
                        )

        # Use Gemini results if available
        if gemini_analysis and "error" not in gemini_analysis:
            logger.info(f"[Macro] Using Gemini analysis for {ticker}")
            
            summary = gemini_analysis.get("summary")
            if not summary:
                # If the LLM returned JSON but missed the summary key, dump the whole response for debugging
                summary = f"Macro analysis completed (Missing summary key). Raw output keys: {list(gemini_analysis.keys())}"
                
            return MacroInsight(
                summary=summary,
                interest_rate_impact=gemini_analysis.get("interest_rate_impact", "Neutral"),
                inflation_impact=gemini_analysis.get("inflation_impact", "Neutral"),
                sector_trend=gemini_analysis.get("sector_trend", "Neutral"),
                macro_bull_case=gemini_analysis.get("macro_bull_case", "Favorable economic conditions."),
                macro_bear_case=gemini_analysis.get("macro_bear_case", "Economic headwinds."),
                confidence=float(gemini_analysis.get("confidence", 0.70)),
                recommendation=gemini_analysis.get("recommendation", "hold").lower(),
                sources=["Gemini Macro-Economic Model"],
            )

        # Fallback: Deterministic analysis
        logger.info(f"[Macro] Using deterministic analysis for {ticker}")
        from hushh_mcp.operons.kai.analysis import analyze_macro

        try:
            analysis = analyze_macro(
                ticker=ticker,
                user_id=user_id,
                market_data=market_data,
                consent_token=consent_token,
                macro_indicators=macro_indicators,
            )

            return MacroInsight(
                summary=analysis.get("summary", f"Deterministic macro analysis for {ticker}."),
                interest_rate_impact=analysis.get("interest_rate_impact", "Unknown due to missing data."),
                inflation_impact=analysis.get("inflation_impact", "Unknown due to missing data."),
                sector_trend=analysis.get("sector_trend", "Market-wide correlation assumed."),
                macro_bull_case=analysis.get("macro_bull_case", "Broad market recovery lifts all assets."),
                macro_bear_case=analysis.get("macro_bear_case", "Systemic shock risks."),
                confidence=float(analysis.get("confidence", 0.40)),
                recommendation=analysis.get("recommendation", "hold").lower(),
                sources=["Deterministic Fallback"],
            )
        except Exception as e:
            logger.error(f"[Macro] Deterministic analysis failed: {e}")
            raise


macro_agent = MacroAgent()
