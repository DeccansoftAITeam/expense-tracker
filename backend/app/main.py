from fastapi import FastAPI

app = FastAPI(title="Expense Tracker API")


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
