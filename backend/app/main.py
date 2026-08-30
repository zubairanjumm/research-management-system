from fastapi import FastAPI

from app.database import Base, engine
from app.routers.projects import router as projects_router

from app.models.project import Project


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ResearchHub API",
    version="1.0.0"
)


app.include_router(projects_router)


@app.get("/")
def root():
    return {"message": "ResearchHub API is running"}