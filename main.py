import os
from fastapi import FastAPI

app = FastAPI()

def mask_secret(value: str):
    if not value:
        return "MISSING"
    # Show first 4 chars to verify it's the right key, hide the rest
    return f"{value[:4]}****************" if len(value) > 4 else "****"

@app.get("/healthz") # Changed to /healthz to match your YAML probe
def health_check():
    return {"status": "healthy"}

@app.get("/env-test")
def read_dummy_env():
    # This will prove if the data is actually arriving in the container
    return {
        "ENV": os.getenv("ENV"),
        "DATABASE_URL_MASKED": mask_secret(os.getenv("DATABASE_URL")),
        "SLACK_CHANNEL": os.getenv("SLACK_ALERT_CHANNEL"),
        "S3_BUCKET": os.getenv("NEUFIN_BACKEND_S3_BUCKET"),
        "S3_REGION": os.getenv("NEUFIN_BACKEND_S3_REGION"),
        "FASTAPI_PORT": os.getenv("PORT")
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
