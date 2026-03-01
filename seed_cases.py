"""
Seed script to populate cases table with initial data
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.case import Case


async def seed_cases():
    """Seed the cases table with initial data"""
    
    cases_data = [
        {
            "name": "Vertex Logistics Corp - $18M Working Capital Facility",
            "description": "Working capital facility for Vertex Logistics Corp with $18 million credit line"
        }
    ]
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if cases already exist
            result = await session.execute(select(Case))
            existing_cases = result.scalars().all()
            
            if existing_cases:
                print(f"Found {len(existing_cases)} existing cases. Skipping seed.")
                return
            
            # Insert new cases
            for case_data in cases_data:
                case = Case(**case_data)
                session.add(case)
            
            await session.commit()
            print(f"Successfully seeded {len(cases_data)} cases!")
            
            # Verify insertion
            result = await session.execute(select(Case))
            all_cases = result.scalars().all()
            
            print("\nSeeded cases:")
            for case in all_cases:
                print(f"  - ID {case.id}: {case.name}")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding cases: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed cases table...")
    await seed_cases()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
