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
    statuses = result.scalars().all()
    
    if not statuses:
        raise NotFoundException(f"Covenant status for case {case_id} not found")
    
    return {
        "data": {
            "caseId": case_id,
            "covenants": [
                {
                    "name": s.name,
                    "label": s.label,
                    "value": s.value
                }
                for s in statuses
            ]
        }
    }
