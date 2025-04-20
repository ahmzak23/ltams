from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Ticket])
def read_tickets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve tickets.
    """
    if crud.user.is_superuser(current_user):
        tickets = crud.ticket.get_multi(db, skip=skip, limit=limit)
    else:
        tickets = crud.ticket.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return tickets

@router.post("/", response_model=schemas.Ticket)
def create_ticket(
    *,
    db: Session = Depends(deps.get_db),
    ticket_in: schemas.TicketCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new ticket.
    """
    ticket = crud.ticket.create_with_user(db=db, obj_in=ticket_in, user_id=current_user.id)
    return ticket

@router.put("/{id}", response_model=schemas.Ticket)
def update_ticket(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    ticket_in: schemas.TicketUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a ticket.
    """
    ticket = crud.ticket.get(db=db, id=id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if not crud.user.is_superuser(current_user) and (ticket.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ticket = crud.ticket.update(db=db, db_obj=ticket, obj_in=ticket_in)
    return ticket

@router.get("/{id}", response_model=schemas.Ticket)
def read_ticket(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get ticket by ID.
    """
    ticket = crud.ticket.get(db=db, id=id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if not crud.user.is_superuser(current_user) and (ticket.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return ticket

@router.delete("/{id}", response_model=schemas.Ticket)
def delete_ticket(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a ticket.
    """
    ticket = crud.ticket.get(db=db, id=id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if not crud.user.is_superuser(current_user) and (ticket.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    ticket = crud.ticket.remove(db=db, id=id)
    return ticket 