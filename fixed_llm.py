# common/llm_adapter.py
import os, requests, json
from typing import List, Tuple
import time

# Use host.docker.internal for Docker container communication
OLLAMA_HOST = "http://host.docker.internal:11434"
OLLAMA_MODEL = "llama3:latest"

def _build_prompt(top_features: List[Tuple[str, float]]) -> str:
    lines = [
        "Explain crop yield factors in simple terms:"
    ]
    for feat, val in top_features[:3]:
        lines.append(f"- {feat}: {val:+.3f}")
    lines.append("Give 2 farming tips.")
    return "\n".join(lines)

def summarize_top_features(top_features: List[Tuple[str, float]]) -> str:
    prompt = _build_prompt(top_features)
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "5m",
        "options": {"num_ctx": 1024}
    }

    for attempt, timeout_s in enumerate([10, 30], start=1):
        try:
            print(f'Attempt {attempt} to call Ollama...')
            r = requests.post(url, json=payload, timeout=timeout_s)
            r.raise_for_status()
            data = r.json()
            text = data.get("response") or json.dumps(data)
            print(f'SUCCESS: Ollama responded on attempt {attempt}')
            return text if isinstance(text, str) else str(text)
        except Exception as e:
            print(f'Attempt {attempt} failed: {e}')
            if attempt == 1:
                time.sleep(1)
                continue
            break

    # fallback
    lines = ["(LLM unavailable - fallback explanation)"]
    for feat, val in top_features:
        sign = "positive" if val >= 0 else "negative"
        lines.append(f"- {feat}: {sign} impact ({val:+.3f})")
    lines.append("Tips: adjust irrigation/fertilizer; monitor soil and weather monthly.")
    return "\n".join(lines)
