#uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from User.user_router import router as user_router
from project.project_router import project_router

from core.database import init_db
from core.config import get_config

routers = []
routers.append(user_router)
routers.append(project_router)
app = FastAPI(
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

for router in routers:
    app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:3000","https://pnn-web-4bad4.web.app"],  # 허용할 출처(이후에 수정할 예정)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db(config=get_config())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
