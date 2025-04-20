from fastapi import APIRouter
from app.api.api_v1.endpoints import users, tickets, auth

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"]) 