"""mermaid_whisperer skill

Provides a tool to extract examples of Mermaid charts from the
assets/examples/mermaid_chart_types.md file and return only the
chart types requested by the caller.

The caller indicates desired chart types by providing a list of
strings (chart type tokens such as "flowchart", "sequenceDiagram",
"gantt", etc.). This is more flexible and extensible than a set of
boolean flags: new chart types can be requested without changing the
function signature.
"""
from typing import List, Optional
import re
from mcp_object import mcp
from response import GlyphMCPResponse
from read_an_asset import read_asset_exact as _read_asset_exact


@mcp.tool()
def mermaid_whisperer(*, 
                      list_available: bool = False,
                      chart_types: Optional[List[str]] = None,
                      include_titles: bool = True) -> GlyphMCPResponse[str]:
    """Give the caller examples of how different mermaid charts look.

    Args:
        list_available: If True, the tool returns a list of available
                        chart types found in the document instead of
                        the chart examples themselves.
        chart_types: Optional list of chart type tokens (case-insensitive).
                     If None or empty, all detected charts are returned.
                     Example tokens: "flowchart", "sequenceDiagram",
                     "stateDiagram-v2", "erDiagram", "gantt", "pie", etc.
        include_titles: If True, the returned text includes the human
                        title that precedes each code block. If False,
                        only the raw ```mermaid ... ``` blocks are returned.

    Returns:
        GlyphMCPResponse containing the concatenated requested chart
        examples (or an informative error context on failure).
    """
    response = GlyphMCPResponse[str]()

    content = _read_asset_exact("examples/mermaid_chart_types.md")
    if content.startswith("Asset file") or content.startswith("Error reading"):
        response.add_context(content)
        return response

    matches = _find_mermaid_blocks(content)
    charts = _build_charts(matches)

    if list_available:
        return _handle_list_available(response, charts)

    return _handle_chart_retrieval(response, matches, charts, chart_types, include_titles)


def _find_mermaid_blocks(content: str) -> List[tuple[str, str]]:
    """Return list of (title, code) tuples for mermaid code blocks in content.

    Prefers titled blocks (a non-code line immediately preceding a code fence).
    Falls back to bare ```mermaid fences with empty title.
    """
    pattern = re.compile(r"(?sm)(?:^|\n)\s*([^\n`].*?)\n```mermaid\s*\n(.*?)\n```")
    matches = pattern.findall(content)
    if matches:
        return [(t, c) for t, c in matches]

    fence_pattern = re.compile(r"(?sm)```mermaid\s*\n(.*?)\n```")
    blocks = fence_pattern.findall(content)
    return [("", b) for b in blocks]


def _detect_token(code: str) -> str:
    first_line = code.strip().splitlines()[0].strip() if code.strip() else ""
    token = first_line.split()[0] if first_line else "unknown"
    return token.lower()


def _build_charts(matches: List[tuple[str, str]]) -> dict[str, List[tuple[str, str]]]:
    charts: dict[str, List[tuple[str, str]]] = {}
    for title, code in matches:
        key = _detect_token(code)
        charts.setdefault(key, []).append((title.strip(), code.rstrip()))
    return charts


def _normalize_requested(chart_types: Optional[List[str]]) -> Optional[set]:
    if not chart_types:
        return None
    return {c.lower() for c in chart_types if c}


def _append_item(out_parts: List[str], title: str, code: str, include_titles: bool) -> None:
    if include_titles and title:
        out_parts.append(title)
    out_parts.append("```mermaid\n" + code + "\n```")


def _handle_list_available(response: GlyphMCPResponse[str], 
                          charts: dict[str, List[tuple[str, str]]]) -> GlyphMCPResponse[str]:
    """Handle the list_available mode - return available chart types."""
    if not charts:
        response.add_context("No mermaid charts found in the document.")
        return response
    available = sorted(set(charts.keys()))
    response.success = True
    response.result = "\n".join(available)
    return response


def _handle_chart_retrieval(response: GlyphMCPResponse[str],
                           matches: List[tuple[str, str]],
                           charts: dict[str, List[tuple[str, str]]],
                           chart_types: Optional[List[str]],
                           include_titles: bool) -> GlyphMCPResponse[str]:
    """Handle the normal mode - retrieve and format chart examples."""
    requested = _normalize_requested(chart_types)
    found_any, out_parts = _collect_outputs(matches, charts, requested, include_titles)

    if requested is not None and not found_any:
        types_str = ", ".join(chart_types) if chart_types else ""
        response.add_context(f"No mermaid charts matching: {types_str}")
        return response

    response.success = True
    response.result = "\n\n".join(out_parts)
    return response


def _collect_outputs(matches: List[tuple[str, str]], charts: dict[str, List[tuple[str, str]]],
                     requested: Optional[set], include_titles: bool) -> tuple[bool, List[str]]:
    out_parts: List[str] = []
    if requested is None or len(requested) == 0:
        for title, code in matches:
            _append_item(out_parts, title, code, include_titles)
        return (True, out_parts)

    found_any = False
    for req in requested:
        if req in charts:
            for t, c in charts[req]:
                _append_item(out_parts, t, c, include_titles)
                found_any = True
        else:
            for k, items in charts.items():
                if k.startswith(req):
                    for t, c in items:
                        _append_item(out_parts, t, c, include_titles)
                        found_any = True

    return (found_any, out_parts)
