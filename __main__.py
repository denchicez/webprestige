import uvicorn

from config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        host=settings.server_host,
        port=settings.server_port,
        workers=1
    )
