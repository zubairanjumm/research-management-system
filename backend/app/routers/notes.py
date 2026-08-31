from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import validate_project
from app.database import get_db
from app.models.note import Note
from app.schemas.note import (
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)
from app.models.project import Project

router = APIRouter(
    prefix="/api/notes",
    tags=["Notes"]
)


@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    validate_project(note.project_id,db)
    new_note = Note(
        project_id=note.project_id,
        title=note.title,
        content=note.content,
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@router.get("/", response_model=list[NoteResponse])
def get_notes(
    project_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Note)

    if project_id is not None:
        query = query.filter(
            Note.project_id == project_id
        )

    return query.all()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id)
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db)
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id)
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    update_data = note_data.model_dump(
        exclude_unset=True
    )
    if "project_id" in update_data:
        validate_project(update_data["project_id"], db)

    for field, value in update_data.items():
        setattr(note, field, value)

    db.commit()
    db.refresh(note)

    return note


@router.delete("/{note_id}", response_model=dict)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id)
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)
    db.commit()

    return {
        "message": "Note deleted successfully"
    }