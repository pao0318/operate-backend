from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.quarterly_dscr import QuarterlyDSCR

router = APIRouter()


@router.get("/{case_id}/quarterly-dscr")
async def get_quarterly_dscr(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(QuarterlyDSCR).where(QuarterlyDSCR.case_id == case_id)
    )
    dscr = result.scalar_one_or_none()
    
    if not dscr:
        raise NotFoundException(f"Quarterly DSCR for case {case_id} not found")
    
    return {
        "data": {
            "caseId": dscr.case_id,
            "dataPoints": dscr.data or []
        }
    }
