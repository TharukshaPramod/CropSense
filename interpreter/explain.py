# interpreter/explain.py
import joblib, numpy as np, pandas as pd
from pathlib import Path
from typing import Dict, Any
from common.llm_adapter import summarize_top_features

MODEL_PATH = Path("predictor/models/model.joblib")
if not MODEL_PATH.exists():
    raise FileNotFoundError("Model not found. Train first.")

artifact = joblib.load(MODEL_PATH)
model = artifact["model"]
feature_columns = artifact["feature_columns"]

def explain_sample(sample: Dict[str, float]) -> Dict[str, Any]:
    # Build array with training order
    row = pd.DataFrame([sample])
    for c in feature_columns:
        if c not in row.columns:
            row[c] = 0
    X = row[feature_columns]

    # Try Tree SHAP (fast for tree models)
    shap_info = None
    top_features = []
    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(X)
        arr = shap_vals[0] if isinstance(shap_vals, (list, tuple)) else shap_vals
        # arr shape: (1, n_features)
        contributions = dict(zip(feature_columns, arr.tolist()[0]))
        ranked = sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True)
        top_features = [(k, float(v)) for k, v in ranked[:5]]
        shap_info = contributions
    except Exception:
        # fallback: feature_importances_
        importances = getattr(model, "feature_importances_", None)
        if importances is not None:
            ranked = sorted(zip(feature_columns, importances), key=lambda kv: abs(kv[1]), reverse=True)
            top_features = [(k, float(v)) for k, v in ranked[:5]]
        else:
            # last resort: differences from population mean
            try:
                df = pd.read_parquet("data/processed/features.parquet")
                means = df[feature_columns].mean()
                diffs = {c: float(abs(X.iloc[0][c] - means[c])) for c in feature_columns}
                ranked = sorted(diffs.items(), key=lambda kv: kv[1], reverse=True)
                top_features = [(k, float(v)) for k, v in ranked[:5]]
            except Exception:
                top_features = [(feature_columns[i], 0.0) for i in range(min(5, len(feature_columns)))]

    # Ask LLM for plain-language summary (prefer Ollama local server; fallback to FLAN-T5)
    summary = summarize_top_features(top_features)
    return {"status": "ok", "top_features": top_features, "summary": summary, "shap_raw": shap_info}
