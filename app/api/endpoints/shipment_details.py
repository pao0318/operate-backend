from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.shipment_detail import ShipmentDetail

router = APIRouter()


@router.get("/{case_id}/shipment-details")
async def get_shipment_details(
    case_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ShipmentDetail).where(ShipmentDetail.case_id == case_id)
    )
    shipments = result.scalars().all()
    
    return {
        "data": {
            "caseId": case_id,
            "shipments": [
                {
                    "id": s.id,
                    "name": s.name,
                    "promisedDeliveryDate": s.promised_delivery_date.isoformat() if s.promised_delivery_date else None,
                    "actualDeliveryDate": s.actual_delivery_date.isoformat() if s.actual_delivery_date else None
                }
                for s in shipments
            ]
        }
    }
