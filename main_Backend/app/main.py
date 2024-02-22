from fastapi import FastAPI
from routers.one_question import one_api_router
from routers.es_upload import es_upload_router
from routers.firebase import firebase_API






try:

    app = FastAPI()

    @app.get("/",tags=["root"])
    async def root():
        return{"data":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}

    app.include_router(one_api_router)
    app.include_router(es_upload_router)
    app.include_router(firebase_API)

except Exception as e:
        print(f"[-]Error during routing at main.py : {str(e)}")
        














