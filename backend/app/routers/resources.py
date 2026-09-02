from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.project import Project
from app.models.resource import Resource
from app.models.user import User
from app.schemas.resource import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)

router = APIRouter(
    prefix="/api/resources",
    tags=["Resources"]
)


@router.post(
    "/",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(
            Project.id == resource.project_id,
            Project.user_id == current_user.id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    new_resource = Resource(
        project_id=resource.project_id,
        title=resource.title,
        description=resource.description,
        url=resource.url,
        resource_type=resource.resource_type,
    )

    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)

    return new_resource


@router.get(
    "/",
    response_model=list[ResourceResponse]
)
def get_resources(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Resource)
        .join(Project)
        .filter(Project.user_id == current_user.id)
    )

    if project_id is not None:
        query = query.filter(Resource.project_id == project_id)

    return query.all()


@router.get(
    "/{resource_id}",
    response_model=ResourceResponse
)
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resource = (
        db.query(Resource)
        .join(Project)
        .filter(
            Resource.id == resource_id,
            Project.user_id == current_user.id
        )
        .first()
    )

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )

    return resource


@router.put(
    "/{resource_id}",
    response_model=ResourceResponse
)
def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resource = (
        db.query(Resource)
        .join(Project)
        .filter(
            Resource.id == resource_id,
            Project.user_id == current_user.id
        )
        .first()
    )

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )

    update_data = resource_data.model_dump(
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
        setattr(resource, field, value)

    db.commit()
    db.refresh(resource)

    return resource


@router.delete(
    "/{resource_id}",
    response_model=dict
)
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resource = (
        db.query(Resource)
        .join(Project)
        .filter(
            Resource.id == resource_id,
            Project.user_id == current_user.id
        )
        .first()
    )

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )

    db.delete(resource)
    db.commit()

    return {
        "message": "Resource deleted successfully"
    }