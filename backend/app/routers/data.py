from fastapi import APIRouter, HTTPException
from backend.app.services.database import db, TABLE_FILES

router=APIRouter(prefix="/data",tags=["Enterprise Data"])

@router.get("/resources")
def resources(): return list(TABLE_FILES.keys())

@router.get("/{resource}")
def get_all(resource:str):
    try: return db.all(resource)
    except ValueError as e: raise HTTPException(404,str(e))

@router.get("/{resource}/{entity_id}")
def get_by_id(resource:str,entity_id:str):
    try: row=db.get(resource,entity_id)
    except ValueError as e: raise HTTPException(404,str(e))
    if not row: raise HTTPException(404,"Entity not found or resource has no single primary key")
    return row
