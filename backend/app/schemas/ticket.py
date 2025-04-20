from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.ticket import TicketStatus

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    quantity: int
    status: TicketStatus = TicketStatus.RESERVED

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    title: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    status: Optional[TicketStatus] = None

class TicketInDBBase(TicketBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Ticket(TicketInDBBase):
    pass 