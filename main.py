import os
from fastapi import FastAPI

app = FastAPI()

def mask_secret(value: str):
    """Shows first 4 chars to verify, hides the rest."""
    if not value or value.strip() == "":
        return "MISSING"
    return f"{value[:4]}****************"

@app.get("/healthz")
def health_check():
    """Matches the startup, readiness, and liveness probes in YAML."""
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Lumen UAT Service is Live"}

@app.get("/env-test")
def read_dummy_env():
    """Verify if secrets are injected into Cloud Run OS environment."""
    return {
        "ENV": os.getenv("ENV"),
        "DATABASE_URL_MASKED": mask_secret(os.getenv("DATABASE_URL")),
        "SLACK_CHANNEL": os.getenv("SLACK_ALERT_CHANNEL"),
        "S3_BUCKET": os.getenv("NEUFIN_BACKEND_S3_BUCKET"),
        "S3_REGION": os.getenv("NEUFIN_BACKEND_S3_REGION"),
        "ANTHROPIC_KEY_MASKED": mask_secret(os.getenv("ANTHROPIC_CLIENT_KEY")),
        "FASTAPI_PORT": os.getenv("PORT")
    }

if __name__ == "__main__":
    import uvicorn
    # PORT is injected by Cloud Run (default 8000)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
