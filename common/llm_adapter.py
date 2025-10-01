# common/llm_adapter.py
import os, requests
from typing import List, Tuple

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
FLAN_MODEL = os.environ.get("FLAN_MODEL", "google/flan-t5-small")

def _call_ollama(prompt: str, model: str = "gemma3") -> str:
    # Ollama's generate API is typically POST /api/generate with JSON like { "model":"llama2", "prompt":"..." }
    try:
        payload = {"model": model, "prompt": prompt, "stream": False}
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=20)
        if r.ok:
            j = r.json()
            # Ollama responses vary; try common fields
            if "response" in j:
                return str(j["response"])
            if "text" in j:
                return str(j["text"])
            # some versions return "result" or nested arrays
            return str(j)
    except Exception:
        raise

def _call_flan(prompt: str) -> str:
    try:
        from transformers import pipeline
        pipe = pipeline("text2text-generation", model=FLAN_MODEL)
        out = pipe(prompt, max_length=150, do_sample=False)
        return out[0]["generated_text"]
    except Exception:
        return ""

def summarize_top_features(top_features: List[Tuple[str, float]]) -> str:
    prompt = "You are an agronomy assistant. Given the top contributing features and their numeric scores, produce a 3-line plain-English summary explaining the likely causes and two practical mitigations a smallholder farmer can do.\n\nTop features:\n"
    for f, s in top_features:
        prompt += f"- {f}: {s:.4f}\n"
    # Try Ollama first
    try:
        text = _call_ollama(prompt, model=os.environ.get("OLLAMA_MODEL", "llama2"))
        if text:
            return text
    except Exception:
        pass
    # Fallback to FLAN
    text = _call_flan(prompt)
    if text:
        return text
    # Final fallback
    return "Top drivers: " + ", ".join([f for f,_ in top_features]) + ". Interpret these accordingly."
