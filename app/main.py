from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import configure_logging
from app.routers import auth, knowledge, mcp, rag, text2sql, viz


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Nutrition Risk Assessment", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth.router)
    app.include_router(knowledge.router)
    app.include_router(rag.router)
    app.include_router(text2sql.router)
    app.include_router(viz.router)
    app.include_router(mcp.router)
    return app


app = create_app()
