from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.project import Project


def validate_project(
    project_id: int,
    db: Session
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project