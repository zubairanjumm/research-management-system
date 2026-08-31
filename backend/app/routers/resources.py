from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import validate_project
from app.database import get_db
from app.models.resource import Resource
from app.schemas.resource import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from app.models.project import Project

router = APIRouter(
    prefix="/api/resources",
    tags=["Resources"]
)

@router.post("/", response_model=ResourceResponse)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db)
):
    validate_project(resource.project_id, db)

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

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return resource


@router.put("/{resource_id}", response_model=ResourceResponse)
def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db)
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    update_data = resource_data.model_dump(
        exclude_unset=True
    )
    if (
        "project_id" in update_data
        and update_data["project_id"] is not None
    ):
        if "project_id" in update_data:
            validate_project(update_data["project_id"],db)
            
    for field, value in update_data.items():
        setattr(resource, field, value)

    db.commit()
    db.refresh(resource)

    return resource


@router.delete("/{resource_id}", response_model=dict)
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    db.delete(resource)
    db.commit()

    return {
        "message": "Resource deleted successfully"
    }

@router.get("/", response_model=list[ResourceResponse])
def get_resources(
    project_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Resource)

    if project_id is not None:
        query = query.filter(Resource.project_id == project_id)

    return query.all()