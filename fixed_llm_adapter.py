import requests
import os
import logging
import json
from typing import Optional

logger = logging.getLogger(__name__)

def generate_llm_explanation(prompt: str, max_retries: int = 2) -> Optional[str]:
    """
    Generate explanation using Ollama LLM with retry logic
    """
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    model = os.getenv("CROPSENSE_OLLAMA_MODEL", "llama3:latest")
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "num_predict": 150
        }
    }
    
    for attempt in range(max_retries):
        try:
            timeout = 15 if attempt == 0 else 45
            logger.info(f"Attempt {attempt + 1} to call Ollama (timeout: {timeout}s)")
            
            response = requests.post(
                f"{ollama_host}/api/generate",
                json=payload,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.warning(f"Ollama returned status {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            logger.warning(f"Ollama timeout on attempt {attempt + 1}")
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama service")
            break
        except Exception as e:
            logger.error(f"Unexpected error calling Ollama: {e}")
            break
    
    logger.error("All Ollama attempts failed, using fallback")
    return None

def _build_prompt(features, top_features, prediction):
    \"\"\"Build a prompt for LLM explanation\"\"\"
    feature_desc = ", ".join([f"{k}: {v}" for k, v in features.items()])
    top_feat_desc = ", ".join([f"{k} ({v:.1f})" for k, v in top_features.items()])
    
    prompt = f\"\"\"Based on these crop features: {feature_desc}

The prediction model estimates a yield of {prediction:.1f} units.
The most influential features are: {top_feat_desc}

Provide a concise 2-3 sentence explanation of why these features affect the yield prediction:\"\"\"
    
    return prompt

def summarize_top_features(features, top_features, prediction):
    \"\"\"Generate LLM summary for top features\"\"\"
    prompt = _build_prompt(features, top_features, prediction)
    explanation = generate_llm_explanation(prompt)
    
    if explanation:
        return explanation
    else:
        # Fallback explanation
        top_feat_names = list(top_features.keys())[:3]
        return f\"The yield prediction is primarily influenced by {', '.join(top_feat_names)}. \" \\
               f\"These factors combined with the specific crop conditions result in the estimated yield of {prediction:.1f} units.\"
