from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RoutePoint(BaseModel):
    lat: float
    lng: float
    orderId: int
    eta: str

@router.get("/routes/{driver_id}")
def get_driver_route(driver_id: int):
    """GET call: returns all orders assigned to driver with driver_id"""
    return []  # list of orders as dicts (dict contains info about order)
