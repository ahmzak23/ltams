from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class User(BaseModel):
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    tickets = relationship("Ticket", back_populates="user") 