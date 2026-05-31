"""Macro agent stream contract tests."""

from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]


def test_analyze_stream_includes_macro_agent():
    analyze_source = (_ROOT / "api/routes/kai/stream.py").read_text(encoding="utf-8")

    # Check that macro agent is initialized
    assert 'macro_agent = MacroAgent(processing_mode="hybrid")' in analyze_source

    # Check that macro agent starts before parallel calls
    gather_index = analyze_source.index("concurrent_results = await asyncio.gather")
    macro_start_index = analyze_source.index('"agent": "macro"')
    assert macro_start_index < gather_index

    # Check that macro agent results are used in debate
    assert "macro_insight=macro_insight" in analyze_source
