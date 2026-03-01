"""
Seed script to populate quarterly_dscr table with quarterly DSCR data
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.quarterly_dscr import QuarterlyDSCR
from app.models.case import Case


async def seed_quarterly_dscr():
    """Seed the quarterly_dscr table with quarterly DSCR data"""
    
    quarterly_dscr_data = [
        {
            "quarter": "Q1",
            "dscr": 1.8,
            "period": "FY 24-25 (Jan - Mar)",
            "threshold": 1.1
        },
        {
            "quarter": "Q2",
            "dscr": 2.4,
            "period": "FY 24-25 (Apr - Jun)",
            "threshold": 1.1
        },
        {
            "quarter": "Q3",
            "dscr": 2.0,
            "period": "FY 24-25 (Jul - Sep)",
            "threshold": 1.1
        },
        {
            "quarter": "Q4",
            "dscr": 1.9,
            "period": "FY 24-25 (Oct - Dec)",
            "threshold": 1.1
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
            
            # Check if quarterly DSCR data already exists for this case
            result = await session.execute(
                select(QuarterlyDSCR).where(QuarterlyDSCR.case_id == case.id)
            )
            existing_record = result.scalars().first()
            
            if existing_record:
                print(f"Found existing quarterly DSCR record for this case. Updating with new data.")
                # Update existing record
                existing_record.data = quarterly_dscr_data
            else:
                print(f"Creating new quarterly DSCR record.")
                # Create new record
                quarterly_dscr = QuarterlyDSCR(
                    case_id=case.id,
                    data=quarterly_dscr_data
                )
                session.add(quarterly_dscr)
            
            await session.commit()
            print(f"Successfully seeded quarterly DSCR data with {len(quarterly_dscr_data)} quarters!")
            
            # Verify insertion
            result = await session.execute(
                select(QuarterlyDSCR).where(QuarterlyDSCR.case_id == case.id)
            )
            saved_record = result.scalars().first()
            
            if saved_record:
                print(f"\nSaved quarterly DSCR data:")
                print(f"  - Case ID: {saved_record.case_id}")
                print(f"  - Data contains {len(saved_record.data)} quarters:")
                for quarter_data in saved_record.data:
                    print(f"    * {quarter_data['quarter']}: DSCR {quarter_data['dscr']} ({quarter_data['period']})")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding quarterly DSCR: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed quarterly_dscr table...")
    await seed_quarterly_dscr()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
