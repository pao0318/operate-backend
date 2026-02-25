from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.fry14_schedule_template import FRY14ScheduleTemplateDataPoint

router = APIRouter()


@router.get("/{case_id}/fr-y14-schedule-template")
async def get_fry14_schedule_template(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(FRY14ScheduleTemplateDataPoint)
        .options(selectinload(FRY14ScheduleTemplateDataPoint.details))
        .where(FRY14ScheduleTemplateDataPoint.case_id == case_id)
    )
    data_points = result.scalars().all()
    
    return {
        "data": {
            "caseId": case_id,
            "dataPoints": [
                {
                    "id": dp.id,
                    "name": dp.name,
                    "label": dp.label,
                    "details": [
                        {
                            "id": detail.id,
                            "name": detail.name,
                            "label": detail.label,
                            "value": detail.value
                        }
                        for detail in dp.details
                    ]
                }
                for dp in data_points
            ]
        }
    }
