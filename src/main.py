if __name__ == "__main__":
    from app.app import app
    from decouple import config
    import uvicorn

    uvicorn.run(app, port=int(config("PORT")))
