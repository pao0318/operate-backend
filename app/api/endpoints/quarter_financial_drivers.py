from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.quarter_financial_drivers import QuarterByQuarterFinancialDrivers

router = APIRouter()


@router.get("/{case_id}/quarter-by-quarter-financial-drivers")
async def get_quarter_financial_drivers(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(QuarterByQuarterFinancialDrivers).where(
            QuarterByQuarterFinancialDrivers.case_id == case_id
        )
    )
    drivers = result.scalar_one_or_none()
    
    if not drivers:
        raise NotFoundException(f"Quarter financial drivers for case {case_id} not found")
    
    return {
        "data": {
            "caseId": drivers.case_id,
            "dataPoints": drivers.data or []
        }
    }
