from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
#import sys
#sys.path.append("..")
from app.models import Note, NoteCreator, NoteUpdater, NoteOuter
from app.database import (
    get_notes,
    get_note,
    create_note,
    update_note,
    delete_note,
)
from app.utils.auth import get_user


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Note not found"}}
)

@router.get("/", response_model=List[NoteOuter])
async def read_notes(user: int = Depends(get_user)):
    notes = await get_notes(user)
    return notes

@router.post("/", response_model=NoteOuter)
async def create_note(note: NoteCreator, user: int = Depends(get_user)):
    note = await create_note(note, user)
    return note


@router.get("/{note_id}", response_model=NoteOuter)
async def read_note(note_id: int, user: int = Depends(get_user)):
    note = await get_note(note_id, user)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteOuter)
async def update_note(note_id: int, note: NoteUpdater, user: int = Depends(get_user)):
    note = await update_note(note_id, note, user)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/{note_id}")
async def delete_note(note_id: int, user: int = Depends(get_user)):
    await delete_note(note_id, user)
    return {"message": "Note deleted successefully"}
    
    
