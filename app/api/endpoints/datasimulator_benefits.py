from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.datasimulator_benefits import DatasimulatorBenefits

router = APIRouter()


@router.get("/{case_id}/data-simulator-benefits")
async def get_datasimulator_benefits(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DatasimulatorBenefits).where(DatasimulatorBenefits.case_id == case_id)
    )
    benefits = result.scalar_one_or_none()
    
    if not benefits:
        raise NotFoundException(f"Data simulator benefits for case {case_id} not found")
    
    data = benefits.data or {}
    
    return {
        "data": {
            "caseId": benefits.case_id,
            "offerings": data.get("offerings", []),
            "speed": data.get("speed", {}),
            "accuracy": data.get("accuracy", {}),
            "compliance": data.get("compliance", {})
        }
    }
