from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate

class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: TicketCreate, user_id: int
    ) -> Ticket:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Ticket]:
        return (
            db.query(self.model)
            .filter(Ticket.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

ticket = CRUDTicket(Ticket) 