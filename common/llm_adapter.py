# common/llm_adapter.py
import os, requests, json
from typing import List, Tuple

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("CROPSENSE_OLLAMA_MODEL", "flan-t5-small")

def _build_prompt(top_features: List[Tuple[str, float]]) -> str:
    lines = [
        "You are an agronomist. Explain in farmer-friendly language why these features affected yield.",
        "Give one line per feature and 2 actionable tips."
    ]
    for feat, val in top_features:
        lines.append(f"- {feat}: {val:+.3f}")
    return "\n".join(lines)

def summarize_top_features(top_features: List[Tuple[str, float]]) -> str:
    prompt = _build_prompt(top_features)
    # Try Ollama local REST API
    try:
        url = f"{OLLAMA_HOST}/api/generate"
        payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        data = r.json()
        # Ollama JSON often contains "response"
        text = data.get("response") or json.dumps(data)
        return text if isinstance(text, str) else str(text)
    except Exception:
        pass

    # fallback static explanation
    lines = ["(LLM unavailable — fallback explanation)"]
    for feat, val in top_features:
        sign = "positive" if val >= 0 else "negative"
        lines.append(f"- {feat}: {sign} impact ({val:+.3f})")
    lines.append("Tips: adjust irrigation/fertilizer; monitor soil & weather monthly.")
    return "\n".join(lines)
