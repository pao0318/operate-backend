from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.models.extracted_key_metrics import ExtractedKeyMetrics

router = APIRouter()


@router.get("/{case_id}/extracted-key-metrics")
async def get_extracted_key_metrics(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ExtractedKeyMetrics).where(ExtractedKeyMetrics.case_id == case_id)
    )
    metrics_list = result.scalars().all()
    
    if not metrics_list:
        raise NotFoundException(f"Extracted key metrics for case {case_id} not found")
    
    return {
        "data": {
            "caseId": case_id,
            "metrics": [
                {
                    "name": m.name,
                    "description": m.description,
                    "dataPoints": m.data or {}
                }
                for m in metrics_list
            ]
        }
    }
