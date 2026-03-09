from pydantic import BaseModel
from typing import Optional, List
from schemas.output_schemas import OrderOutput

class ValidationIssue(BaseModel):
    field: str
    severity: str
    message: str
    suggestion: Optional[str] = None

class OrderCreationResponse(BaseModel):
    success: bool
    order: Optional[OrderOutput] = None
    issues: List[ValidationIssue] = []