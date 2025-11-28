"""Minimal Anthropic Claude client for generating human-like report text.

Reads `CLAUDE_API_KEY` from the environment. Sends a prompt containing the
structured report JSON and returns the assistant text. This is a conservative
implementation using `urllib` so it has no extra dependencies.
"""
import json
import os
import urllib.request
import urllib.error
from typing import Any, Optional


API_URL = os.getenv("CLAUDE_API_URL", "https://api.anthropic.com/v1/complete")
API_KEY_ENV = "CLAUDE_API_KEY"


def _build_prompt(report_type: str, data: Any, tone: str = "friendly") -> str:
    instruction = (
        "You are an analytics assistant. Produce a concise, human-friendly report "
        "summary based on the JSON data below. Use plain language and highlight the most important points."
    )
    note = (
        "Do not output the JSON back. Keep it short (2-4 sentences). "
        f"Use a {tone} tone."
    )
    payload = json.dumps({"report_type": report_type, "data": data}, default=str)
    prompt = f"{instruction}\n{note}\n\nJSON:\n{payload}\n\nSummary:\n"
    return prompt


def generate_report_with_claude(report_type: str, data: Any, tone: str = "friendly", max_tokens: int = 512) -> Optional[str]:
    """Send structured report `data` to Claude and return the generated summary text.

    Raises RuntimeError on missing API key or HTTP errors.
    Returns None only in unexpected cases where the response body can't be parsed.
    """
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing Claude API key: set the {API_KEY_ENV} environment variable")

    prompt = _build_prompt(report_type, data, tone=tone)

    body = {
        "model": "claude-2",
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens,
        "temperature": 0.3,
    }

    data_bytes = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data_bytes, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-API-Key", api_key)
    req.add_header("User-Agent", "retailbrain/claude-client")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode("utf-8")
            try:
                parsed = json.loads(resp_body)
            except Exception:
                # If API returns plain text, return it.
                return resp_body.strip()

            # Look for common text fields used by different Claude response shapes
            for key in ("completion", "output", "text", "completion_text", "response"):
                if key in parsed and isinstance(parsed[key], str):
                    return parsed[key].strip()

            choices = parsed.get("choices") or parsed.get("outputs")
            if isinstance(choices, list) and choices:
                first = choices[0]
                if isinstance(first, dict):
                    for k in ("text", "output", "content"):
                        if k in first and isinstance(first[k], str):
                            return first[k].strip()
                elif isinstance(first, str):
                    return first.strip()

            # Fallback: return raw body
            return resp_body.strip()

    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8') if hasattr(e, 'read') else ''
        raise RuntimeError(f"Claude API HTTP error: {e.code} - {e.reason} - {body}")
    except Exception as e:
        raise RuntimeError(f"Claude request failed: {e}")
