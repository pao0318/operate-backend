"""
Seed script to populate q3_highlights table with Q3 highlight data
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.q3_highlight import Q3Highlight
from app.models.case import Case


async def seed_q3_highlights():
    """Seed the q3_highlights table with Q3 highlight data"""
    
    q3_highlights_data = [
        {
            "name": "DSCR Improvement",
            "description": "DSCR increased from 1.10 in Q2 → 1.15 in Q3, driven by higher operating cash flow.",
            "datalines": [
                "DSCR increased from 1.10 in Q2 → 1.15 in Q3",
                "Driven by higher operating cash flow"
            ]
        },
        {
            "name": "Cash Flow Growth",
            "description": "Operating cash flow rose to $22K, marking a +22% increase quarter-over-quarter.",
            "datalines": [
                "Operating cash flow rose to $22K",
                "Marking a +22% increase quarter-over-quarter"
            ]
        },
        {
            "name": "Interest Costs Stabilized",
            "description": "Interest expense increased only slightly ($4.0K → $4.5K), slowing the negative pressure on coverage.",
            "datalines": [
                "Interest expense increased only slightly ($4.0K → $4.5K)",
                "Slowing the negative pressure on coverage"
            ]
        },
        {
            "name": "Delayed Shipments Reduced",
            "description": "Shipment delays dropped from 5 to 3, contributing to stronger cash collections.",
            "datalines": [
                "Shipment delays dropped from 5 to 3",
                "Contributing to stronger cash collections"
            ]
        },
        {
            "name": "Operating Revenue Rebounded",
            "description": "Revenue improved following improved fulfillment performance (Promised vs Delivered variance reduced by 8%).",
            "datalines": [
                "Revenue improved following improved fulfillment performance",
                "Promised vs Delivered variance reduced by 8%"
            ]
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
            
            # Check if Q3 highlights already exist for this case
            result = await session.execute(
                select(Q3Highlight).where(Q3Highlight.case_id == case.id)
            )
            existing_records = result.scalars().all()
            
            if existing_records:
                print(f"Found {len(existing_records)} existing Q3 highlight records. Skipping seed.")
                return
            
            # Create Q3 highlight records
            highlight_records = []
            for highlight in q3_highlights_data:
                record = Q3Highlight(
                    case_id=case.id,
                    name=highlight['name'],
                    description=highlight['description'],
                    datalines=highlight['datalines']
                )
                highlight_records.append(record)
            
            # Insert all records
            for record in highlight_records:
                session.add(record)
            
            await session.commit()
            print(f"Successfully seeded {len(highlight_records)} Q3 highlight records!")
            
            # Verify insertion
            result = await session.execute(
                select(Q3Highlight).where(Q3Highlight.case_id == case.id)
            )
            saved_records = result.scalars().all()
            
            print("\nSeeded Q3 highlight records:")
            for record in saved_records:
                print(f"  - ID {record.id}: {record.name}")
                print(f"    Description: {record.description[:80]}...")
                print(f"    Data lines: {len(record.datalines)} items")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding Q3 highlights: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed q3_highlights table...")
    await seed_q3_highlights()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
