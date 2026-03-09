from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class CommitChangesInput(BaseModel):
    driver_id: int
    assigned_order_ids: List[int]  # new orders list

@router.post("/commit")
def commit_manual_changes(payload: CommitChangesInput):
    """POST call: inserts new custom order sequence into the DB."""
    return {}