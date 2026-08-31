from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResourceCreate(BaseModel):
    project_id: int
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    url: str = Field(min_length=1, max_length=500)
    resource_type: str = Field(min_length=1, max_length=50)


class ResourceUpdate(BaseModel):
    project_id: int | None = None
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )
    description: str | None = Field(
        default=None,
        min_length=1
    )
    url: str | None = Field(
        default=None,
        min_length=1,
        max_length=500
    )
    resource_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )


class ResourceResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: str
    url: str
    resource_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)