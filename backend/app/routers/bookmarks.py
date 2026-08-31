from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import validate_project
from app.database import get_db
from app.models.bookmark import Bookmark
from app.schemas.bookmarks import (
    BookmarkCreate,
    BookmarkResponse,
    BookmarkUpdate,
)
from app.models.project import Project

router = APIRouter(
    prefix="/api/bookmarks",
    tags=["Bookmarks"]
)


@router.post("/", response_model=BookmarkResponse)
def create_bookmark(
    bookmark: BookmarkCreate,
    db: Session = Depends(get_db)
):
    validate_project(bookmark.project_id,db)

    new_bookmark = Bookmark(
        project_id=bookmark.project_id,
        title=bookmark.title,
        url=bookmark.url,
        description=bookmark.description,
    )

    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)

    return new_bookmark


@router.get("/", response_model=list[BookmarkResponse])
def get_bookmarks(
    project_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Bookmark)

    if project_id is not None:
        query = query.filter(
            Bookmark.project_id == project_id
        )

    return query.all()


@router.get("/{bookmark_id}", response_model=BookmarkResponse)
def get_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db)
):
    bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.id == bookmark_id)
        .first()
    )

    if bookmark is None:
        raise HTTPException(
            status_code=404,
            detail="Bookmark not found"
        )

    return bookmark


@router.put("/{bookmark_id}", response_model=BookmarkResponse)
def update_bookmark(
    bookmark_id: int,
    bookmark_data: BookmarkUpdate,
    db: Session = Depends(get_db)
):
    bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.id == bookmark_id)
        .first()
    )

    if bookmark is None:
        raise HTTPException(
            status_code=404,
            detail="Bookmark not found"
        )

    update_data = bookmark_data.model_dump(
        exclude_unset=True
    )
    if "project_id" in update_data:
        validate_project(update_data["project_id"], db)

    for field, value in update_data.items():
        setattr(bookmark, field, value)

    db.commit()
    db.refresh(bookmark)

    return bookmark


@router.delete("/{bookmark_id}", response_model=dict)
def delete_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db)
):
    bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.id == bookmark_id)
        .first()
    )

    if bookmark is None:
        raise HTTPException(
            status_code=404,
            detail="Bookmark not found"
        )

    db.delete(bookmark)
    db.commit()

    return {
        "message": "Bookmark deleted successfully"
    }