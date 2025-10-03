# interpreter/explain.py
import joblib, numpy as np, pandas as pd
from pathlib import Path
from typing import Dict, Any
from common.llm_adapter import summarize_top_features

MODEL_PATH = Path("predictor/models/model.joblib")

def _load_artifact():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)

def explain_sample(sample: Dict[str, float]) -> Dict[str, Any]:
    artifact = _load_artifact()
    if artifact is None:
        return {"status": "error", "detail": "Model not found. Train first."}

    model = artifact["model"]
    feature_columns = artifact["feature_columns"]
    preproc = artifact.get("preprocessor", {})
    encoders = preproc.get("encoders")
    imputer = preproc.get("imputer")
    scaler = preproc.get("scaler")
    num_cols = preproc.get("num_cols")

    # prepare DataFrame and apply same transforms as predictor
    row = pd.DataFrame([sample])
    for c in feature_columns:
        if c not in row.columns:
            row[c] = 0

    # booleans -> numeric - FIXED: Use proper dtype conversion
    for bcol in ["Fertilizer_Used", "Irrigation_Used"]:
        if bcol in row.columns:
            val = row.at[0, bcol]
            if pd.isna(val):
                row.at[0, bcol] = np.nan
            else:
                if isinstance(val, str):
                    lv = val.lower()
                    if lv in ("true", "1", "yes"):
                        row.at[0, bcol] = 1.0
                    elif lv in ("false", "0", "no"):
                        row.at[0, bcol] = 0.0
                    else:
                        row.at[0, bcol] = np.nan
                else:
                    # Convert to float first to avoid dtype warning
                    row.at[0, bcol] = float(bool(val))

    if encoders:
        for c, mapping in encoders.items():
            if c not in row.columns:
                row[c] = np.nan
            else:
                raw_val = row.at[0, c]
                if pd.isna(raw_val):
                    row.at[0, c] = np.nan
                else:
                    mapped = mapping.get(raw_val)
                    if mapped is None and isinstance(raw_val, str):
                        found = None
                        for k in mapping.keys():
                            if isinstance(k, str) and k.lower() == raw_val.lower():
                                found = mapping[k]
                                break
                        row.at[0, c] = float(found) if found is not None else np.nan
                    else:
                        row.at[0, c] = float(mapped) if mapped is not None else np.nan

    if num_cols and imputer is not None and scaler is not None:
        for c in num_cols:
            if c not in row.columns:
                row[c] = np.nan
        X_num = row[num_cols].astype(float)
        try:
            X_num_imputed = imputer.transform(X_num)
            X_num_scaled = scaler.transform(X_num_imputed)
            for i, c in enumerate(num_cols):
                row.at[0, c] = float(X_num_scaled[0, i])
        except Exception:
            row[num_cols] = row[num_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0)

    # compute explanation (shap if available)
    top_features = []
    shap_info = None
    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(row[feature_columns])
        arr = shap_vals[0] if isinstance(shap_vals, (list, tuple)) else shap_vals
        contributions = dict(zip(feature_columns, arr.tolist()[0]))
        ranked = sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True)
        top_features = [(k, float(v)) for k, v in ranked[:5]]
        shap_info = contributions
    except Exception:
        importances = getattr(model, "feature_importances_", None)
        if importances is not None:
            ranked = sorted(zip(feature_columns, importances), key=lambda kv: abs(kv[1]), reverse=True)
            top_features = [(k, float(v)) for k, v in ranked[:5]]
        else:
            try:
                df = pd.read_parquet("data/processed/features.parquet")
                means = df[feature_columns].mean()
                diffs = {c: float(abs(row.iloc[0][c] - means[c])) for c in feature_columns}
                ranked = sorted(diffs.items(), key=lambda kv: kv[1], reverse=True)
                top_features = [(k, float(v)) for k, v in ranked[:5]]
            except Exception:
                top_features = [(feature_columns[i], 0.0) for i in range(min(5, len(feature_columns)))]

    summary = summarize_top_features(top_features)
    return {"status": "ok", "top_features": top_features, "summary": summary, "shap_raw": shap_info}