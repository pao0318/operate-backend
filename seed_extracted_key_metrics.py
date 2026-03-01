"""
Seed script to populate extracted_key_metrics table with financial data from data.json
"""
import asyncio
import json
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.extracted_key_metrics import ExtractedKeyMetrics
from app.models.case import Case


async def seed_extracted_key_metrics():
    """Seed the extracted_key_metrics table with financial data"""
    
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
            
            # Check if extracted key metrics already exist for this case
            result = await session.execute(
                select(ExtractedKeyMetrics).where(ExtractedKeyMetrics.case_id == case.id)
            )
            existing_metrics = result.scalars().first()
            
            if existing_metrics:
                print(f"Found existing extracted key metrics for this case. Updating with new data.")
                # Update existing record
                existing_metrics.name = "Financial Metrics Dashboard"
                existing_metrics.description = "Key financial metrics including Revenue, EBITDA, Debt, Equity, and Interest Expense"
                existing_metrics.data = financial_data
            else:
                print(f"Creating new extracted key metrics record.")
                # Create new record
                metrics = ExtractedKeyMetrics(
                    case_id=case.id,
                    name="Financial Metrics Dashboard",
                    description="Key financial metrics including Revenue, EBITDA, Debt, Equity, and Interest Expense",
                    data=financial_data
                )
                session.add(metrics)
            
            await session.commit()
            print(f"Successfully seeded extracted key metrics with {len(financial_data)} financial metrics!")
            
            # Verify insertion
            result = await session.execute(
                select(ExtractedKeyMetrics).where(ExtractedKeyMetrics.case_id == case.id)
            )
            saved_metrics = result.scalars().first()
            
            if saved_metrics:
                print(f"\nSaved metrics:")
                print(f"  - Name: {saved_metrics.name}")
                print(f"  - Description: {saved_metrics.description}")
                print(f"  - Data contains {len(saved_metrics.data)} metrics:")
                for metric in saved_metrics.data:
                    print(f"    * {metric['name']}: {len(metric['dataPoints'])} data points")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding extracted key metrics: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed extracted_key_metrics table...")
    await seed_extracted_key_metrics()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
