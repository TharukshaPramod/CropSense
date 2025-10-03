# common/llm_adapter.py
import os, requests, json
from typing import List, Tuple
import time
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Use environment variables with fallbacks for Docker container communication
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.environ.get("CROPSENSE_OLLAMA_MODEL", "llama3:latest")

def _build_prompt(top_features: List[Tuple[str, float]]) -> str:
    """Build a prompt for LLM explanation"""
    lines = [
        "Explain crop yield factors in simple terms:"
    ]
    for feat, val in top_features[:3]:  # Limit to top 3 features
        lines.append(f"- {feat}: {val:+.3f}")
    lines.append("Give 2 farming tips.")
    return "\n".join(lines)

def summarize_top_features(top_features: List[Tuple[str, float]]) -> str:
    """Generate LLM summary for top features with retry logic"""
    prompt = _build_prompt(top_features)
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "5m",  # Keep model warm for subsequent calls
        "options": {"num_ctx": 1024}  # Small context for speed
    }

    logger.info(f"Calling Ollama at {url} with model {OLLAMA_MODEL}")

    for attempt, timeout_s in enumerate([15, 45], start=1):
        try:
            logger.info(f"Attempt {attempt} to call Ollama (timeout: {timeout_s}s)")
            r = requests.post(url, json=payload, timeout=timeout_s)
            r.raise_for_status()
            data = r.json()
            text = data.get("response") or json.dumps(data)
            logger.info(f"Ollama response successful on attempt {attempt}")
            return text if isinstance(text, str) else str(text)
        except requests.exceptions.Timeout:
            logger.warning(f"Ollama timeout on attempt {attempt}")
            if attempt == 1:
                time.sleep(0.5)  # Brief pause before retry
                continue
            break
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama service")
            break
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt}: {e}")
            if attempt == 1:
                time.sleep(0.5)
                continue
            break

    # Fallback explanation when LLM is unavailable
    logger.warning("Using fallback explanation - Ollama unavailable")
    lines = ["(LLM unavailable - fallback explanation)"]
    for feat, val in top_features:
        sign = "positive" if val >= 0 else "negative"
        lines.append(f"- {feat}: {sign} impact ({val:+.3f})")
    lines.append("Tips: adjust irrigation/fertilizer; monitor soil and weather monthly.")
    return "\n".join(lines)