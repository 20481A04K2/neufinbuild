import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Just to verify env vars are loading (Don't expose real secrets in production logs!)
@app.on_event("startup")
async def startup_event():
    slack_channel = os.getenv("SLACK_ALERT_CHANNEL", "Not Set")
    print(f"Server starting... Slack Channel is: {slack_channel}")
    print(f"Environment is: {os.getenv('ENV', 'Unknown')}")

@app.get("/")
def read_root():
    return {"message": "Hello from GCP Cloud Run! Deployment successful."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/env-test")
def read_dummy_env():
    # Helper to see if our dummy variables exist
    return {
        "database": os.getenv("DATABASE_URL"),
        "slack_token_present": bool(os.getenv("SLACK_BOT_TOKEN")),
        "dummy_key": os.getenv("API_KEY")
    }

if __name__ == "__main__":
    import uvicorn
    # Cloud Run expects us to listen on the port defined by PORT env var, or default 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
