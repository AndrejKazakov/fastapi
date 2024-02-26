import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.router import router as jwt_router

app = FastAPI()

app.include_router(router=jwt_router)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/axios-test/")
def get_response():
    return {"message": "done"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
