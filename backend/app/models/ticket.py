from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel

class TicketStatus(str, enum.Enum):
    RESERVED = "reserved"
    PAID = "paid"
    CANCELLED = "cancelled"

class Ticket(BaseModel):
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.RESERVED)
    
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="tickets") 