# orchestrator/run_pipeline.py
import os, time, requests, sys

COLLECTOR = os.environ.get("COLLECTOR_URL", "http://collector:8001")
PREPROCESSOR = os.environ.get("PREPROCESSOR_URL", "http://preprocessor:8002")
PREDICTOR = os.environ.get("PREDICTOR_URL", "http://predictor:8003")

def wait_for(url, timeout=60):
    end = time.time() + timeout
    while time.time() < end:
        try:
            r = requests.get(url + "/health", timeout=5)
            if r.ok:
                print(f"{url} is up")
                return True
        except Exception:
            pass
        time.sleep(1)
    print(f"Timeout waiting for {url}")
    return False

def main():
    if not wait_for(COLLECTOR): sys.exit(1)
    if not wait_for(PREPROCESSOR): sys.exit(1)
    if not wait_for(PREDICTOR): sys.exit(1)

    print("Triggering collector.collect (local source)")
    r = requests.post(COLLECTOR + "/collect", json={"source":"local"}, timeout=30)
    print("collector:", r.status_code, r.text)

    print("Triggering preprocessor")
    r2 = requests.post(PREPROCESSOR + "/preprocess", json={}, timeout=300)
    print("preprocess:", r2.status_code, r2.text)

    print("Triggering predictor train")
    r3 = requests.post(PREDICTOR + "/train", json={}, timeout=600)
    print("train:", r3.status_code, r3.text)

if __name__ == "__main__":
    main()
