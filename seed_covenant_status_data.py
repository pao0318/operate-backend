"""
Seed script to populate covenant_status table with specific covenant data
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.covenant_status import CovenantStatus
from app.models.case import Case


async def seed_covenant_status_data():
    """Seed the covenant_status table with specific covenant data"""
    
    covenant_data = [
        {
            "name": "DSCR",
            "label": "DSCR",
            "value": "1.10(Below 1.25 Covenant)"
        },
        {
            "name": "Debt/Equity",
            "label": "Debt/Equity", 
            "value": "3.2x(Above 3.0 Threshold)"
        },
        {
            "name": "Current Ratio",
            "label": "Current Ratio",
            "value": "12.3(Unusually high vs. 1.5–2.0 industry norm)"
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
            
            # Check if covenant status records already exist for this case
            result = await session.execute(
                select(CovenantStatus).where(CovenantStatus.case_id == case.id)
            )
            existing_records = result.scalars().all()
            
            if existing_records:
                print(f"Found {len(existing_records)} existing covenant status records. Skipping seed.")
                return
            
            # Create covenant status records
            covenant_records = []
            for covenant in covenant_data:
                record = CovenantStatus(
                    case_id=case.id,
                    name=covenant['name'],
                    label=covenant['label'],
                    value=covenant['value']
                )
                covenant_records.append(record)
            
            # Insert all records
            for record in covenant_records:
                session.add(record)
            
            await session.commit()
            print(f"Successfully seeded {len(covenant_records)} covenant status records!")
            
            # Verify insertion
            result = await session.execute(
                select(CovenantStatus).where(CovenantStatus.case_id == case.id)
            )
            saved_records = result.scalars().all()
            
            print("\nSeeded covenant status records:")
            for record in saved_records:
                print(f"  - ID {record.id}: {record.label} - {record.value}")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding covenant status: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed covenant_status table...")
    await seed_covenant_status_data()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
