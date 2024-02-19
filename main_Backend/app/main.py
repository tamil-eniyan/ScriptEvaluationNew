from fastapi import FastAPI
from routers.one_question import one_api_router








app = FastAPI()

@app.get("/",tags=["root"])
async def root():
    return{"data":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}

app.include_router(one_api_router)
















