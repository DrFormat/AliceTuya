import os

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.asgi:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "8000")),
        reload=True
    )
