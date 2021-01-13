
from fastapi import FastAPI

from pathlib import Path


from fastapi.middleware.cors import CORSMiddleware
from routers import pdf

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8081",
    "http://localhost:1337",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# async def get_token_header(x_token: str = Header(...)):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")

app.include_router(
    pdf.router,
    tags=["PDF"]
)











