from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.available_service import AvailableService
from app.schemas.available_service import AvailableServiceResponse

router = APIRouter()


@router.get("")
async def get_available_services(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AvailableService))
    services = result.scalars().all()
    
    return {
        "data": {
            "services": [
                AvailableServiceResponse.from_orm(s).dict()
                for s in services
            ]
        }
    }
