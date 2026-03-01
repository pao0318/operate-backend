"""
Seed script to populate shipment_details table with shipment data from screenshot
"""
import asyncio
from datetime import date
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.shipment_detail import ShipmentDetail
from app.models.case import Case


async def seed_shipment_details():
    """Seed the shipment_details table with shipment data"""
    
    # Data from screenshot
    shipment_data = [
        {
            "name": "Shipment 1",
            "promised_delivery_date": date(2025, 8, 12),
            "actual_delivery_date": date(2025, 8, 10),
            "status": "Early"
        },
        {
            "name": "Shipment 2",
            "promised_delivery_date": date(2025, 6, 2),
            "actual_delivery_date": date(2025, 6, 1),
            "status": "On-Time"
        },
        {
            "name": "Shipment 3",
            "promised_delivery_date": date(2025, 5, 1),
            "actual_delivery_date": date(2025, 5, 10),
            "status": "Delayed"
        },
        {
            "name": "Shipment 4",
            "promised_delivery_date": date(2025, 4, 12),
            "actual_delivery_date": date(2025, 4, 12),
            "status": "On-Time"
        },
        {
            "name": "Shipment 5",
            "promised_delivery_date": date(2025, 3, 25),
            "actual_delivery_date": date(2025, 3, 25),
            "status": "On-Time"
        },
        {
            "name": "Shipment 6",
            "promised_delivery_date": date(2025, 2, 14),
            "actual_delivery_date": date(2025, 2, 18),
            "status": "Delayed"
        },
        {
            "name": "Shipment 7",
            "promised_delivery_date": date(2025, 2, 2),
            "actual_delivery_date": date(2025, 2, 2),
            "status": "On-Time"
        },
        {
            "name": "Shipment 9",
            "promised_delivery_date": date(2025, 1, 26),
            "actual_delivery_date": date(2025, 1, 26),
            "status": "On-Time"
        }
    ]
    
    async with AsyncSessionLocal() as session:
        try:
            # Get the first case (Vertex Logistics Corp)
            result = await session.execute(select(Case))
            case = result.scalars().first()
            
            if not case:
                print("Error: No case found. Please seed cases first.")
                return
            
            print(f"Using case: {case.name} (ID: {case.id})")
            
            # Check if shipment details already exist for this case
            result = await session.execute(
                select(ShipmentDetail).where(ShipmentDetail.case_id == case.id)
            )
            existing_records = result.scalars().all()
            
            if existing_records:
                print(f"Found {len(existing_records)} existing shipment detail records. Skipping seed.")
                return
            
            # Create shipment detail records
            shipment_records = []
            for shipment in shipment_data:
                record = ShipmentDetail(
                    case_id=case.id,
                    name=shipment['name'],
                    promised_delivery_date=shipment['promised_delivery_date'],
                    actual_delivery_date=shipment['actual_delivery_date'],
                    status=shipment['status']
                )
                shipment_records.append(record)
            
            # Insert all records
            for record in shipment_records:
                session.add(record)
            
            await session.commit()
            print(f"Successfully seeded {len(shipment_records)} shipment detail records!")
            
            # Verify insertion
            result = await session.execute(
                select(ShipmentDetail).where(ShipmentDetail.case_id == case.id)
            )
            saved_records = result.scalars().all()
            
            print("\nSeeded shipment detail records:")
            for record in saved_records:
                print(f"  - {record.name}: Promised {record.promised_delivery_date}, Actual {record.actual_delivery_date}, Status: {record.status}")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding shipment details: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed shipment_details table...")
    await seed_shipment_details()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
