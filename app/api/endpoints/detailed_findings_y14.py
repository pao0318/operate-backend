from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.detailed_findings_y14 import DetailedFindingsY14

router = APIRouter()


@router.get("/{case_id}/y14-detailed-findings")
async def get_detailed_findings_y14(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DetailedFindingsY14).where(DetailedFindingsY14.case_id == case_id)
    )
    findings = result.scalar_one_or_none()
    
    if not findings:
        raise NotFoundException(f"Y14 detailed findings for case {case_id} not found")
    
    data = findings.data or {}
    
    return {
        "data": {
            "caseId": findings.case_id,
            "warningMessage": data.get("warningMessage"),
            "detailedFindings": data.get("detailedFindings", [])
        }
    }
