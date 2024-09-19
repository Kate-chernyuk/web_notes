import json
from typing import List, Optional
from fastapi import HTTPException, status
from app.models import Note, NoteCreator, NoteUpdater
from app.utils.spellcheck import check_spelling

DATA_FILE = "notes.json"


async def get_notes(user_id: int):
    notes = load_notes()
    return [note for note in notes if note.user_id == user_id]


async def get_note(note_id: int, user_id: int):
    notes = load_notes()
    for note in notes:
        if (note.user_id == user_id) and (note.id == note_id):
            return note
    return None


async def create_note(note: NoteCreator, user_id: int):
    notes = load_notes()
    new_id = max([note.id for note in notes], default=0) + 1
    note = Note(id=new_id, title=note.title, content=note.content, user_id=user_id)
    notes.append(note)
    save_notes(notes)
    return note


async def update_note(note_id: int, note: NoteUpdater, user_id: int):
    notes = load_notes()
    for i, n in enumerate(notes):
        if n.id == note_id and n.user_id == user_id:
            if note.title is not None:
                notes[i].title = note.title
            if note.content is not None:
                notes[i].content = note.content
            save_notes(notes)
            return notes[i]
    return None


async def delete_note(note_id: int, user_id: int):
    notes = load_notes()
    new_notes = [note for note in notes if note.user_id != user_id and note.id != note_id]
    save_notes(new_notes)


async def load_notes():
    try:
        with open(DATA_FILE, "r") as file:
            return [Note(**note) for note in json.load(file)]
    except FileNotFoundError:
        return []


async def save_notes(notes):
    with open(DATA_FILE, "w") as file:
        json.dump([note.dict() for note in notes], f, indent=4)

                
            
