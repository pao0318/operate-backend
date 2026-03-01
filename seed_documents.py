"""
Seed script to populate documents table with initial data
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.document import Document
from app.models.case import Case


async def seed_documents():
    """Seed the documents table with initial data"""
    
    documents_data = [
        {
            "name": "Loan Agreement",
            "filename": "Loan_Agreement.pdf",
            "type": "pdf",
            "description": "Primary loan agreement document outlining terms and conditions"
        },
        {
            "name": "Financial Statement",
            "filename": "Financial_Statement.pdf",
            "type": "pdf",
            "description": "Company financial statements and performance metrics"
        },
        {
            "name": "Covenant Summary",
            "filename": "Covenant_Summary.xlsx",
            "type": "xlsx",
            "description": "Summary of loan covenants and compliance tracking"
        },
        {
            "name": "ESG Report 02",
            "filename": "ESG_Report_02.pdf",
            "type": "pdf",
            "description": "Environmental, Social, and Governance report"
        },
        {
            "name": "FR Y-14 Analysis",
            "filename": "FR_Y_14_Analysis.pdf",
            "type": "pdf",
            "description": "Federal Reserve Y-14 regulatory analysis and reporting"
        },
        {
            "name": "Risk Assessment",
            "filename": "Risk_Assessment.docx",
            "type": "docx",
            "description": "Comprehensive risk assessment document"
        },
        {
            "name": "Balance Sheet",
            "filename": "Balance_Sheet.xlsx",
            "type": "xlsx",
            "description": "Company balance sheet and financial position"
        },
        {
            "name": "Quarterly Report",
            "filename": "Quarterly_Report.pdf",
            "type": "pdf",
            "description": "Quarterly financial and operational report"
        },
        {
            "name": "Compliance Certificate",
            "filename": "Compliance_Certificate.pdf",
            "type": "pdf",
            "description": "Compliance certification and regulatory documentation"
        },
        {
            "name": "Market Analysis",
            "filename": "Market_Analysis.pptx",
            "type": "pptx",
            "description": "Market analysis and industry trends presentation"
        },
        {
            "name": "Credit Approval",
            "filename": "Credit_Approval.pdf",
            "type": "pdf",
            "description": "Credit approval documentation and decision rationale"
        },
        {
            "name": "Facility Agreement",
            "filename": "Facility_Agreement.pdf",
            "type": "pdf",
            "description": "Facility agreement terms and conditions"
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
            
            # Check if documents already exist for this case
            result = await session.execute(
                select(Document).where(Document.case_id == case.id)
            )
            existing_documents = result.scalars().all()
            
            if existing_documents:
                print(f"Found {len(existing_documents)} existing documents for this case. Skipping seed.")
                return
            
            # Insert new documents
            for doc_data in documents_data:
                doc_data['case_id'] = case.id
                document = Document(**doc_data)
                session.add(document)
            
            await session.commit()
            print(f"Successfully seeded {len(documents_data)} documents!")
            
            # Verify insertion
            result = await session.execute(
                select(Document).where(Document.case_id == case.id)
            )
            all_documents = result.scalars().all()
            
            print("\nSeeded documents:")
            for doc in all_documents:
                print(f"  - ID {doc.id}: {doc.name} ({doc.filename})")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding documents: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed documents table...")
    await seed_documents()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
