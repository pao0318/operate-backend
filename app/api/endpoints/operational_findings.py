from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.detailed_findings_operational import DetailedFindingsOperational

router = APIRouter()


@router.get("/{case_id}/operational-doc-scan-detailed-findings")
async def get_operational_findings(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DetailedFindingsOperational).where(
            DetailedFindingsOperational.case_id == case_id
        )
    )
    findings = result.scalars().all()
    
    return {
        "data": {
            "caseId": case_id,
            "findings": [f.data for f in findings if f.data]
        }
    }
