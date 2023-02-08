from fastapi import FastAPI
from routes.stoloto import stoloto

app = FastAPI()
app.include_router(stoloto)
