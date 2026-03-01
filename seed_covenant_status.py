"""
Seed script to populate covenant_status table with individual records for each financial metric
"""
import asyncio
import json
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.covenant_status import CovenantStatus
from app.models.case import Case


async def seed_covenant_status():
    """Seed the covenant_status table with individual financial metric records"""
    
    # Load financial data from data.json
    try:
        with open('app/data.json', 'r') as f:
            financial_data = json.load(f)
    except FileNotFoundError:
        print("Error: data.json file not found in app directory")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing data.json: {e}")
        return
    
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
            
            # Create individual records for each financial metric
            covenant_records = []
            for metric in financial_data:
                # Create a covenant status record for each metric
                record = CovenantStatus(
                    case_id=case.id,
                    name=metric['name'],
                    label=f"{metric['name']} Status",
                    value=json.dumps(metric['dataPoints'])  # Store data points as JSON string
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
                print(f"  - ID {record.case_id}: {record.name} - {record.label}")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding covenant status: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed covenant_status table...")
    await seed_covenant_status()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
