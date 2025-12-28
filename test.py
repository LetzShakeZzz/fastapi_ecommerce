from fastapi import APIRouter, Depends, HTTPException, status
from database import get_async_db
from app.schemas.ticket import TicketSchema, TicketCreate
from app.models.ticket import TicketModel
from app.models.user import UserModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post('/', response_model=TicketSchema, status_code=status.HTTP_201_CREATED)
async def get_active_message(
    ticket: TicketCreate, 
    db: AsyncSession = Depends(get_async_db)
):
    find_user = await db.scalars(
        select(UserModel)
        .where(
            UserModel.id == ticket.user_id, 
            UserModel.is_active
        )
    )
    
    user = find_user.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db_ticket = TicketModel(**ticket.model_dump())
    db.add(db_ticket)
    await db.commit()

    return db_ticket
   