from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.bookmark import Bookmark
from app.models.project import Project
from app.models.user import User
from app.schemas.bookmarks import (
    BookmarkCreate,
    BookmarkResponse,
    BookmarkUpdate,
)

router = APIRouter(
    prefix="/api/bookmarks",
    tags=["Bookmarks"]
)


@router.post(
    "/",
    response_model=BookmarkResponse,
    status_code=status.HTTP_201_CREATED
)
def create_bookmark(
    bookmark: BookmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(
            Project.id == bookmark.project_id,
            Project.user_id == current_user.id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

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


@router.get(
    "/",
    response_model=list[BookmarkResponse]
)
def get_bookmarks(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Bookmark)
        .join(Project)
        .filter(Project.user_id == current_user.id)
    )

    if project_id is not None:
        query = query.filter(
            Bookmark.project_id == project_id
        )

    return query.all()


@router.get(
    "/{bookmark_id}",
    response_model=BookmarkResponse
)
def get_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookmark = (
        db.query(Bookmark)
        .join(Project)
        .filter(
            Bookmark.id == bookmark_id,
            Project.user_id == current_user.id
        )
        .first()
    )

    if bookmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )

    return bookmark


@router.put(
    "/{bookmark_id}",
    response_model=BookmarkResponse
)
def update_bookmark(
    bookmark_id: int,
    bookmark_data: BookmarkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookmark = (
        db.query(Bookmark)
        .join(Project)
        .filter(
            Bookmark.id == bookmark_id,
            Project.user_id == current_user.id
        )
        .first()
    )

    if bookmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )

    update_data = bookmark_data.model_dump(
        exclude_unset=True
    )

    if "project_id" in update_data:
        new_project_id = update_data["project_id"]

        project = (
            db.query(Project)
            .filter(
                Project.id == new_project_id,
                Project.user_id == current_user.id
            )
            .first()
        )

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

    for field, value in update_data.items():
        setattr(bookmark, field, value)

    db.commit()
    db.refresh(bookmark)

    return bookmark


@router.delete(
    "/{bookmark_id}",
    response_model=dict
)
def delete_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookmark = (
        db.query(Bookmark)
        .join(Project)
        .filter(
            Bookmark.id == bookmark_id,
            Project.user_id == current_user.id
        )
        .first()
    )

    if bookmark is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )

    db.delete(bookmark)
    db.commit()

    return {
        "message": "Bookmark deleted successfully"
    }
