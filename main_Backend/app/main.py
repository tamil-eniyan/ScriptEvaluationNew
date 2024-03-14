from fastapi import FastAPI
from routers.one_question import one_api_router
from routers.es_upload import es_upload_router
from routers.as_upload import as_upload_router
from routers.geminievaluate import geminiEvaluate_api_router
from routers.firebase import firebase_API
from fastapi.middleware.cors import CORSMiddleware






try:

    app = FastAPI()
    origins = [
         "http://localhost:5173"
    ]
    app.add_middleware(
         CORSMiddleware,
         allow_origins = ["*"],
         allow_credentials = True,
         allow_headers = ["*"],
         allow_methods = ["*"]
    )

    @app.get("/",tags=["root"])
    async def root():
        return{"data":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}

    app.include_router(one_api_router)
    app.include_router(es_upload_router)
    app.include_router(as_upload_router)
    app.include_router(firebase_API)
    app.include_router(geminiEvaluate_api_router)

except Exception as e:
        print(f"[-]Error during routing at main.py : {str(e)}")
        














