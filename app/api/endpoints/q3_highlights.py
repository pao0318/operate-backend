from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.q3_highlight import Q3Highlight

router = APIRouter()


@router.get("/{case_id}/q3-highlights")
async def get_q3_highlights(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Q3Highlight).where(Q3Highlight.case_id == case_id)
    )
    highlights = result.scalars().all()
    
    if not highlights:
        raise NotFoundException(f"Q3 highlights for case {case_id} not found")
    
    return {
        "data": {
            "caseId": case_id,
            "highlights": [
                {
                    "name": h.name,
                    "description": h.description,
                    "datalines": h.datalines or []
                }
                for h in highlights
            ]
        }
    }
