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
    
    # Check if data contains the full metrics array (with infoLines)
    all_metrics = []
    for m in metrics_list:
        if m.data and isinstance(m.data, list):
            # This is the full metrics data with infoLines
            for metric in m.data:
                all_metrics.append({
                    "name": metric.get("name"),
                    "infoLines": metric.get("infoLines", []),
                    "dataPoints": metric.get("dataPoints", {})
                })
        elif m.data and isinstance(m.data, dict):
            # Individual metric with dataPoints only
            all_metrics.append({
                "name": m.name,
                "infoLines": [],
                "dataPoints": m.data
            })
    
    # Remove duplicates by name, preferring entries with infoLines
    seen = {}
    for metric in all_metrics:
        name = metric.get("name")
        if name not in seen or (metric.get("infoLines") and not seen[name].get("infoLines")):
            seen[name] = metric
    
    return {
        "data": {
            "caseId": case_id,
            "metrics": list(seen.values())
        }
    }
