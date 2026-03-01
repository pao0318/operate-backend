"""
Seed script to populate detailed_findings_y14 table with detailed findings data
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.detailed_findings_y14 import DetailedFindingsY14
from app.models.case import Case


async def seed_detailed_findings_y14():
    """Seed the detailed_findings_y14 table with detailed findings data"""
    
    # Data structure based on screenshots
    detailed_findings_data = {
        "warningMessage": "Some documents require attention for Y-14 compliance",
        "detailedFindings": [
            {
                "docName": "Finance_Operations_Q2.xlsx",
                "description": "Cash Flow Statement (Operating Activities)",
                "usedFor": "DSCR calculation (EBITDA ÷ Debt Service)"
            },
            {
                "docName": "Loan_Agreement.pdf",
                "description": "Financial Covenant Schedule",
                "usedFor": "Covenant threshold: DSCR ≥ 1.25"
            },
            {
                "docName": "Covenant_Compliance_Certificate_Q2.pdf",
                "description": "Borrower attestation & covenant reporting",
                "usedFor": "Y-14Q Schedule H.1 - Covenant Status"
            },
            {
                "docName": "Borrower_Financials_Q2_Reviewed.pdf",
                "description": "Financial Covenant Schedule",
                "usedFor": "Covenant threshold: DSCR ≥ 1.25"
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
            
            # Check if detailed findings already exist for this case
            result = await session.execute(
                select(DetailedFindingsY14).where(DetailedFindingsY14.case_id == case.id)
            )
            existing_record = result.scalars().first()
            
            if existing_record:
                print(f"Found existing detailed findings record for this case. Updating with new data.")
                existing_record.data = detailed_findings_data
            else:
                print(f"Creating new detailed findings record.")
                detailed_findings = DetailedFindingsY14(
                    case_id=case.id,
                    data=detailed_findings_data
                )
                session.add(detailed_findings)
            
            await session.commit()
            print(f"Successfully seeded detailed findings Y14 data!")
            
            # Verify insertion
            result = await session.execute(
                select(DetailedFindingsY14).where(DetailedFindingsY14.case_id == case.id)
            )
            saved_record = result.scalars().first()
            
            if saved_record:
                print(f"\nSaved detailed findings Y14 data:")
                print(f"  - Case ID: {saved_record.case_id}")
                print(f"  - Warning Message: {saved_record.data.get('warningMessage', 'N/A')}")
                print(f"  - Detailed Findings: {len(saved_record.data.get('detailedFindings', []))} items")
                for finding in saved_record.data.get('detailedFindings', []):
                    print(f"    * Doc: {finding['docName']}")
                    print(f"      Description: {finding['description']}")
                    print(f"      Used For: {finding['usedFor']}")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding detailed findings Y14: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed detailed_findings_y14 table...")
    await seed_detailed_findings_y14()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
