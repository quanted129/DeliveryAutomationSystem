from pydantic import BaseModel
from datetime import datetime

class OrderOutput(BaseModel):
    """Schema for providing cleaned order data format (for UI)"""
    orderId: int
    shopId: int
    address: str
    latitude: float
    longitude: float
    startTime: datetime
    endTime: datetime

    class Config:
        from_attributes = True