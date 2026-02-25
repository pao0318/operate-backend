from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.covenant_status import CovenantStatus

router = APIRouter()


@router.get("/{case_id}/covenant-status")
async def get_covenant_status(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(CovenantStatus).where(CovenantStatus.case_id == case_id)
    )
    status = result.scalar_one_or_none()
    
    if not status:
        raise NotFoundException(f"Covenant status for case {case_id} not found")
    
    return {
        "data": {
            "caseId": status.case_id,
            "name": status.name,
            "label": status.label,
            "value": status.value
        }
    }
