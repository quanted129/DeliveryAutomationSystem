from pydantic import BaseModel, field_validator
from datetime import datetime

class FormOrderInput(BaseModel):
    """Schema for raw order data input checking"""
    shopId: int
    startTime: datetime
    endTime: datetime
    itemInfo: str
    driverInfo: str
    address: str
    type: int

    @field_validator('endTime', mode='after')
    @classmethod
    def is_end_after_start(cls, end: datetime, values):
        """Check if interval's start time is before the end time"""
        if end <= values.data['startTime']:
            raise ValueError(f"Interval's end time ({end}) must be after the start time ({values.data['startTime']})!")
        return end

    # To-do:
    # check to allow one-sided intervals when type = 1 (stretch to ... minutes, print action!)
    # ...