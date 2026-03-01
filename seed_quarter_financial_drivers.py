"""
Seed script to populate quarter_by_quarter_financial_drivers table with financial drivers data
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.quarter_financial_drivers import QuarterByQuarterFinancialDrivers
from app.models.case import Case


async def seed_quarter_financial_drivers():
    """Seed the quarter_by_quarter_financial_drivers table with financial drivers data"""
    
    financial_drivers_data = [
        {
            "quarter": "Q1",
            "cashFlow": 2000,
            "interest": 3000,
            "debt": 10000
        },
        {
            "quarter": "Q2",
            "cashFlow": 3500,
            "interest": 4500,
            "debt": 12000
        },
        {
            "quarter": "Q3",
            "cashFlow": 5000,
            "interest": 6000,
            "debt": 14000
        },
        {
            "quarter": "Q4",
            "cashFlow": 6500,
            "interest": 7000,
            "debt": 13000
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
            
            # Check if quarter financial drivers data already exists for this case
            result = await session.execute(
                select(QuarterByQuarterFinancialDrivers).where(QuarterByQuarterFinancialDrivers.case_id == case.id)
            )
            existing_record = result.scalars().first()
            
            if existing_record:
                print(f"Found existing quarter financial drivers record for this case. Updating with new data.")
                # Update existing record
                existing_record.data = financial_drivers_data
            else:
                print(f"Creating new quarter financial drivers record.")
                # Create new record
                quarter_financial_drivers = QuarterByQuarterFinancialDrivers(
                    case_id=case.id,
                    data=financial_drivers_data
                )
                session.add(quarter_financial_drivers)
            
            await session.commit()
            print(f"Successfully seeded quarter financial drivers data with {len(financial_drivers_data)} quarters!")
            
            # Verify insertion
            result = await session.execute(
                select(QuarterByQuarterFinancialDrivers).where(QuarterByQuarterFinancialDrivers.case_id == case.id)
            )
            saved_record = result.scalars().first()
            
            if saved_record:
                print(f"\nSaved quarter financial drivers data:")
                print(f"  - Case ID: {saved_record.case_id}")
                print(f"  - Data contains {len(saved_record.data)} quarters:")
                for quarter_data in saved_record.data:
                    print(f"    * {quarter_data['quarter']}: Cash Flow ${quarter_data['cashFlow']}, Interest ${quarter_data['interest']}, Debt ${quarter_data['debt']}")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding quarter financial drivers: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed quarter_by_quarter_financial_drivers table...")
    await seed_quarter_financial_drivers()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
