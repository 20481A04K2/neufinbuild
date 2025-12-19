import os
from fastapi import FastAPI
from dotenv import load_dotenv

# IMPORTANT: Load the .env file as early as possible
# This looks for a file named ".env" in the same directory
load_dotenv()

app = FastAPI()

def mask_secret(value: str):
    """Shows first 4 chars to verify, hides the rest."""
    if not value or value.strip() == "":
        return "MISSING"
    return f"{value[:4]}****************"

@app.get("/healthz")
def health_check():
    """FastAPI health endpoint for Cloud Run Probes."""
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Lumen UAT Service is Live (via .env file)"}

@app.get("/env-test")
def read_dummy_env():
    """Verify if secrets are successfully loaded from the .env file."""
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
    # PORT is usually provided by Cloud Run, default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
