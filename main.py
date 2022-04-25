from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database.engine import Base
from app.router.api import router


class MainClass:
    def application():
        app = FastAPI(
            title="Vulnerability Detail", 
            docs_url="/api/vuln/docs", 
            openapi_url="/api/vuln/openapi.json",
            servers=[
                {"url": "http://127.0.0.1:9999", "description": "Local Environment"},
                {"url": "https://37a6-36-80-240-9.ngrok.io ", "description": "Ngrok Environment"}
            ])
        
        #mount static files
        app.mount("/assets", StaticFiles(directory="assets"), name="assets")
        templates = Jinja2Templates(directory="templates")
        
        #tampilan halaman dokumentasi
        @app.get("/", response_class=HTMLResponse)
        async def main(request: Request):
            return templates.TemplateResponse("index.html",{"request":request})
        
        @app.get("/about/", response_class=HTMLResponse)
        async def about(request: Request):
            return templates.TemplateResponse("about/index.html",{"request":request})

        @app.get("/feature/", response_class=HTMLResponse)
        async def about(request: Request):
            return templates.TemplateResponse("feature/index.html",{"request":request})


        app.include_router(
            router=router,
            prefix="/api/vuln")

        app.add_middleware(
            middleware_class=CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        return app

app = MainClass.application()

if __name__ == '__main__':
    run(app=app)