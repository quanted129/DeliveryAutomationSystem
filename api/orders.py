from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List
from db.database import get_db
from db.classes import Order
from schemas.input_schemas import FormOrderInput
from schemas.output_schemas import OrderOutput
from schemas.validation_schemas import OrderCreationResponse, ValidationIssue
from services.data_validator import validate_and_prepare_order, ValidationError


router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]

@router.get("/awaiting", response_model=List[OrderOutput])
def get_awaiting_orders(db: DbSession):
    """GET call: returns all orders where driverId = null"""
    orders = db.query(Order).filter(Order.driverId.is_(None)).all()
    return orders


@router.post("/add", response_model=OrderCreationResponse)
def create_new_order(raw_order: FormOrderInput, db: DbSession):
    """POST call: add new order and check its validity"""
    issues = []

    try:
        validated_db_dict = validate_and_prepare_order(raw_order, db)

        if validated_db_dict.get('distance', 0) > 300:  # MAKE DYNAMIC
            issues.append(ValidationIssue(
                field="address", severity="warning",
                message="Distance exceeds 300km.", suggestion="Verify address text."
            ))

        new_order = Order(**validated_db_dict)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return OrderCreationResponse(success=True, order=new_order, issues=issues)

    except ValidationError as e:  # show warning in UI
        issues.append(ValidationIssue(
            field="general", severity="error", message=str(e), suggestion="Check input fields."
        ))
        return OrderCreationResponse(success=False, issues=issues)