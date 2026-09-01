from fastapi import FastAPI

from app.routers.projects import router as projects_router
from app.routers.resources import router as resources_router
from app.routers.notes import router as notes_router
from app.routers.bookmarks import router as bookmarks_router
from app.routers.auth import router as auth_router

from app.models.project import Project
from app.models.resource import Resource
from app.models.note import Note
from app.models.bookmark import Bookmark
from app.models.user import User


app = FastAPI(
    title="ResearchHub API",
    version="1.0.0"
)


app.include_router(projects_router)
app.include_router(resources_router)
app.include_router(notes_router)
app.include_router(bookmarks_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "ResearchHub API is running"}