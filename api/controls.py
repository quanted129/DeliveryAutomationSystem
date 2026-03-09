from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SystemMode(BaseModel):
    is_automatic: bool
    system_disabled: bool

@router.post("/mode")
def update_operation_mode(mode: SystemMode):
    """POST call: switches on or off the program or the automatic routing engine."""
    return {"message": "Mode updated successfully", "current_mode": mode}