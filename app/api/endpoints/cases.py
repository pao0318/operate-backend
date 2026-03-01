from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.case import Case
from app.schemas.case import CaseResponse

router = APIRouter()


@router.get("/{case_id}")
async def get_case(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    
    if not case:
        raise NotFoundException(f"Case with id {case_id} not found")
    
    return {
        "data": {
            "case": CaseResponse.from_orm(case).dict()
        }
    }
