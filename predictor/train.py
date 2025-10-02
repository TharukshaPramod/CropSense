# predictor/train.py
import os, joblib, math
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROCESSED = Path("data/processed/features.parquet")
MODEL_DIR = Path("predictor/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "model.joblib"

COMMON_MODELS = Path("common/models")
COMMON_MODELS.mkdir(parents=True, exist_ok=True)

def train_and_save(use_lightgbm=True):
    if not PROCESSED.exists():
        raise FileNotFoundError("Processed data not found, run preprocessor first.")
    df = pd.read_parquet(PROCESSED)

    # target detection
    if "Yield_tons_per_hectare" in df.columns:
        target = "Yield_tons_per_hectare"
    elif "yield" in df.columns:
        target = "yield"
    else:
        raise ValueError("Target column not found. Expected 'Yield_tons_per_hectare' or 'yield'.")

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

    model = None
    try:
        if use_lightgbm:
            import lightgbm as lgb
            model = lgb.LGBMRegressor(n_estimators=1000, learning_rate=0.05, n_jobs=-1, verbose=-1)
            # ✅ new LightGBM syntax for early stopping
            model.fit(
                X_train, y_train,
                eval_set=[(X_valid, y_valid)],
                callbacks=[lgb.early_stopping(stopping_rounds=50)]
            )
        else:
            raise ImportError("lightgbm disabled")
    except Exception as e:
        print("LightGBM not available or failed — falling back to RandomForest:", e)
        model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

    preds = model.predict(X_valid)
    mae = mean_absolute_error(y_valid, preds)
    rmse = math.sqrt(mean_squared_error(y_valid, preds))
    r2 = r2_score(y_valid, preds)

    # Load preprocessor artifacts (encoders etc.)
    imputer = scaler = encoders = num_cols = None
    for name in ["imputer", "scaler", "encoders", "num_cols"]:
        try:
            locals()[name] = joblib.load(COMMON_MODELS / f"{name}.joblib")
        except Exception:
            locals()[name] = None

    artifact = {
        "model": model,
        "feature_columns": X.columns.tolist(),
        "preprocessor": {
            "imputer": imputer,
            "scaler": scaler,
            "encoders": encoders,
            "num_cols": num_cols,
        }
    }
    joblib.dump(artifact, MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")
    print(f"MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")
    return {"mae": mae, "rmse": rmse, "r2": r2}

if __name__ == "__main__":
    train_and_save()
