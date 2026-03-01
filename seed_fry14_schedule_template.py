"""
Seed script to populate FR Y-14 Schedule Template tables with data from screenshots
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.fry14_schedule_template import FRY14ScheduleTemplateDataPoint, FRY14ScheduleTemplateDataPointDetail
from app.models.case import Case


async def seed_fry14_schedule_template():
    """Seed the FR Y-14 Schedule Template tables with data from screenshots"""
    
    # Data structure: Each accordion section with its details
    schedule_template_data = [
        {
            "name": "Borrower / Obligor Information",
            "label": "Borrower / Obligor Information",
            "details": [
                {"name": "Obligor name", "label": "Obligor name", "value": "Vertex Logistics Corp."},
                {"name": "Obligor ID", "label": "Obligor ID", "value": "00492-WHSL"},
                {"name": "Country", "label": "Country", "value": "United States"},
                {"name": "Industry/NAICS code", "label": "Industry/NAICS code", "value": "488510 - Freight Transportation Arrangement"},
                {"name": "Obligor type", "label": "Obligor type", "value": "Corporate"}
            ]
        },
        {
            "name": "Loan Characteristics",
            "label": "Loan Characteristics",
            "details": [
                {"name": "Loan Type", "label": "Loan Type", "value": "Working Capital Revolver"},
                {"name": "Origination Date", "label": "Origination Date", "value": "15-Jan-21"},
                {"name": "Maturity Date", "label": "Maturity Date", "value": "15-Jan-26"},
                {"name": "Original Commitment", "label": "Original Commitment", "value": "$1,80,00,000"},
                {"name": "Current Outstanding Balance", "label": "Current Outstanding Balance", "value": "$1,42,00,000"}
            ]
        },
        {
            "name": "Collateral Information",
            "label": "Collateral Information",
            "details": [
                {"name": "Collateral Type", "label": "Collateral Type", "value": "Accounts Receivable + Inventory"},
                {"name": "Collateral Code", "label": "Collateral Code", "value": "24"},
                {"name": "Collateral Value", "label": "Collateral Value", "value": "$2,10,00,000"},
                {"name": "LTV (Calculated)", "label": "LTV (Calculated)", "value": "64%"},
                {"name": "Lien Position", "label": "Lien Position", "value": "1st Lien"}
            ]
        },
        {
            "name": "Covenant Information (Extracted)",
            "label": "Covenant Information (Extracted)",
            "details": [
                {
                    "name": "DSCR",
                    "label": "DSCR",
                    "value": None,
                    "additional_data": {
                        "covenant": "DSCR",
                        "threshold": "≥ 1.20",
                        "current": "0.75",
                        "status": "At Risk"
                    }
                },
                {
                    "name": "LTV",
                    "label": "LTV",
                    "value": None,
                    "additional_data": {
                        "covenant": "LTV",
                        "threshold": "≤ 70%",
                        "current": "64%",
                        "status": "Compliant"
                    }
                },
                {
                    "name": "Leverage Ratio",
                    "label": "Leverage Ratio",
                    "value": None,
                    "additional_data": {
                        "covenant": "Leverage Ratio",
                        "threshold": "≤ 3.50x",
                        "current": "3.20x",
                        "status": "Compliant"
                    }
                }
            ]
        },
        {
            "name": "Credit Quality & Risk Metrics",
            "label": "Credit Quality & Risk Metrics",
            "details": [
                {"name": "Internal Risk Rating", "label": "Internal Risk Rating", "value": "6 (Moderate Risk)"},
                {"name": "Prob. of Default (PD)", "label": "Prob. of Default (PD)", "value": "1.90%"},
                {"name": "Loss Given Default (LGD)", "label": "Loss Given Default (LGD)", "value": "38%"},
                {"name": "Exposure at Default (EAD)", "label": "Exposure at Default (EAD)", "value": "$1,80,00,000"},
                {"name": "Accrued Interest", "label": "Accrued Interest", "value": "$72,400"}
            ]
        },
        {
            "name": "Performance & Payment Info",
            "label": "Performance & Payment Info",
            "details": [
                {"name": "Days Past Due", "label": "Days Past Due", "value": "0"},
                {"name": "Past Due Indicator", "label": "Past Due Indicator", "value": "No"},
                {"name": "Last Payment Date", "label": "Last Payment Date", "value": "12-Sep-25"},
                {"name": "Next Payment Date", "label": "Next Payment Date", "value": "12-Oct-25"},
                {"name": "Payment Status", "label": "Payment Status", "value": "Current"}
            ]
        },
        {
            "name": "Accounting & Reporting Attributes",
            "label": "Accounting & Reporting Attributes",
            "details": [
                {"name": "Accounting Standard", "label": "Accounting Standard", "value": "GAAP"},
                {"name": "Accrual Status", "label": "Accrual Status", "value": "Performing"},
                {"name": "Impairment Status", "label": "Impairment Status", "value": "Not Impaired"},
                {"name": "Charge-Off Amount", "label": "Charge-Off Amount", "value": "$0"},
                {"name": "Restructured Indicator", "label": "Restructured Indicator", "value": "No"}
            ]
        },
        {
            "name": "Regulatory Schedule Mapping (Meta Fields)",
            "label": "Regulatory Schedule Mapping (Meta Fields)",
            "details": [
                {"name": "DSCR (Reported)", "label": "DSCR (Reported)", "value": "0.75"},
                {"name": "DSCR (Trend YoY)", "label": "DSCR (Trend YoY)", "value": "5%"},
                {"name": "LTV (Reported)", "label": "LTV (Reported)", "value": "64%"},
                {"name": "EBITDA (TTM)", "label": "EBITDA (TTM)", "value": "$1.2B"},
                {"name": "Revenue (TTM)", "label": "Revenue (TTM)", "value": "$12.5B"}
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
            
            # Check if FR Y-14 schedule template data already exists for this case
            result = await session.execute(
                select(FRY14ScheduleTemplateDataPoint).where(FRY14ScheduleTemplateDataPoint.case_id == case.id)
            )
            existing_records = result.scalars().all()
            
            if existing_records:
                print(f"Found {len(existing_records)} existing FR Y-14 schedule template records. Skipping seed.")
                return
            
            # Create parent records (accordion headers) and their details
            total_details = 0
            for section in schedule_template_data:
                # Create parent record
                data_point = FRY14ScheduleTemplateDataPoint(
                    case_id=case.id,
                    name=section['name'],
                    label=section['label']
                )
                session.add(data_point)
                await session.flush()  # Get the ID for the parent record
                
                # Create detail records
                for detail in section['details']:
                    detail_record = FRY14ScheduleTemplateDataPointDetail(
                        template_data_point_id=data_point.id,
                        name=detail['name'],
                        label=detail['label'],
                        value=detail.get('value'),
                        additional_data=detail.get('additional_data')
                    )
                    session.add(detail_record)
                    total_details += 1
                
                print(f"  Created: {section['name']} with {len(section['details'])} details")
            
            await session.commit()
            print(f"\nSuccessfully seeded {len(schedule_template_data)} accordion sections with {total_details} total detail records!")
            
            # Verify insertion
            result = await session.execute(
                select(FRY14ScheduleTemplateDataPoint).where(FRY14ScheduleTemplateDataPoint.case_id == case.id)
            )
            saved_records = result.scalars().all()
            
            print("\nSeeded FR Y-14 Schedule Template sections:")
            for record in saved_records:
                print(f"  - ID {record.id}: {record.name}")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding FR Y-14 schedule template: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed FR Y-14 Schedule Template tables...")
    await seed_fry14_schedule_template()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
