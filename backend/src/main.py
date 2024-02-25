import uvicorn
from fastapi import FastAPI

from auth.router import router as jwt_router

app = FastAPI()

app.include_router(router=jwt_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
