from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.services.supabase import supabase_client

from app.routers.techArticles import techRouter
from app.routers.financeArticles import financeRouter

origins = [
    'http://localhost:5173'
]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(techRouter)
app.include_router(financeRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)