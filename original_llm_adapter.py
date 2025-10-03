# common/llm_adapter.py
import os, requests, json
from typing import List, Tuple
import time

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("CROPSENSE_OLLAMA_MODEL", "llama3")

def _build_prompt(top_features: List[Tuple[str, float]]) -> str:
    lines = [
        "Explain crop yield factors in simple terms:"
    ]
    for feat, val in top_features[:3]:  # Limit to top 3 features
        lines.append(f"- {feat}: {val:+.3f}")
    lines.append("Give 2 farming tips.")
    return "\n".join(lines)

def summarize_top_features(top_features: List[Tuple[str, float]]) -> str:
    prompt = _build_prompt(top_features)
    # Try Ollama local REST API with a quick attempt, then a longer warm-load attempt
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        # keep model in memory for a bit to avoid reload cost on subsequent calls
        "keep_alive": "5m",
        # small context by default for speed
        "options": {"num_ctx": 1024}
    }

    for attempt, timeout_s in enumerate([15, 45], start=1):
        try:
            r = requests.post(url, json=payload, timeout=timeout_s)
            r.raise_for_status()
            data = r.json()
            text = data.get("response") or json.dumps(data)
            return text if isinstance(text, str) else str(text)
        except Exception:
            # brief pause before retrying with a longer timeout
            if attempt == 1:
                time.sleep(0.5)
                continue
            break

    # fallback static explanation
    lines = ["(LLM unavailable — fallback explanation)"]
    for feat, val in top_features:
        sign = "positive" if val >= 0 else "negative"
        lines.append(f"- {feat}: {sign} impact ({val:+.3f})")
    lines.append("Tips: adjust irrigation/fertilizer; monitor soil & weather monthly.")
    return "\n".join(lines)
