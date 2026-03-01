"""
Seed script to populate detailed_findings_operational table with operational findings data from screenshots
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.detailed_findings_operational import DetailedFindingsOperational
from app.models.case import Case


async def seed_detailed_findings_operational():
    """Seed the detailed_findings_operational table with operational findings data"""
    
    # Data structure based on screenshots
    detailed_findings_data = {
        "warningMessage": "Operational metrics require attention for performance optimization",
        "detailedFindings": [
            {
                "docName": "On-Time Delivery (OTIF) Impact",
                "description": "Tracking OTIF dropped to 91%, missing covenant threshold",
                "usedFor": "Analyze root cause: late pickups, route inefficiency, or carrier performance"
            },
            {
                "docName": "Promised vs Delivered Variance",
                "description": "Delivery lead times vary ±60% (2-10 days), impacting cash flow",
                "usedFor": "Standardize lead time estimates and improve forecasting accuracy"
            },
            {
                "docName": "Cost Per Mile / Unit Cost Pressure",
                "description": "Analyze cost per mile vs 8.5 p/mi, understand if cost pressure exists",
                "usedFor": "Identify cost drivers: fuel, labor, maintenance, or route optimization gaps"
            },
            {
                "docName": "Capacity Utilization Decline",
                "description": "Flagging utilization at 78%, impacting fixed cost absorption",
                "usedFor": "Review load planning and asset allocation to improve utilization rates"
            },
            {
                "docName": "OTIF Gap/Time to Fulfil",
                "description": "Tracking OTIF at 91% (Above 90%)",
                "usedFor": "Monitor performance trends and identify improvement opportunities"
            }
        ]
    }
    
    async with AsyncSessionLocal() as session:
        try:
            # Get the first case (Vertex Logistics Corp)
            result = await session.execute(select(Case))
            case = result.scalars().first()
            
            if not case:
                print("Error: No case found. Please seed cases first.")
                return
            
            print(f"Using case: {case.name} (ID: {case.id})")
            
            # Check if detailed findings operational already exist for this case
            result = await session.execute(
                select(DetailedFindingsOperational).where(DetailedFindingsOperational.case_id == case.id)
            )
            existing_record = result.scalars().first()
            
            if existing_record:
                print(f"Found existing detailed findings operational record for this case. Updating with new data.")
                existing_record.data = detailed_findings_data
            else:
                print(f"Creating new detailed findings operational record.")
                detailed_findings = DetailedFindingsOperational(
                    case_id=case.id,
                    data=detailed_findings_data
                )
                session.add(detailed_findings)
            
            await session.commit()
            print(f"Successfully seeded detailed findings operational data!")
            
            # Verify insertion
            result = await session.execute(
                select(DetailedFindingsOperational).where(DetailedFindingsOperational.case_id == case.id)
            )
            saved_record = result.scalars().first()
            
            if saved_record:
                print(f"\nSaved detailed findings operational data:")
                print(f"  - Case ID: {saved_record.case_id}")
                print(f"  - Warning Message: {saved_record.data.get('warningMessage', 'N/A')}")
                print(f"  - Detailed Findings: {len(saved_record.data.get('detailedFindings', []))} items")
                for finding in saved_record.data.get('detailedFindings', []):
                    print(f"    * Doc: {finding['docName']}")
                    print(f"      Description: {finding['description']}")
                    print(f"      Used For: {finding['usedFor']}")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding detailed findings operational: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed detailed_findings_operational table...")
    await seed_detailed_findings_operational()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
