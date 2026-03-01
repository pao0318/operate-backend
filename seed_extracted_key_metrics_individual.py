"""
Seed script to populate extracted_key_metrics table with individual records for each financial metric
"""
import asyncio
import json
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.extracted_key_metrics import ExtractedKeyMetrics
from app.models.case import Case


async def seed_extracted_key_metrics_individual():
    """Seed the extracted_key_metrics table with individual financial metric records"""
    
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
            existing_records = result.scalars().all()
            
            if existing_records:
                print(f"Found {len(existing_records)} existing extracted key metrics records. Skipping seed.")
                return
            
            # Create individual records for each financial metric
            metric_records = []
            for metric in financial_data:
                # Create an extracted key metrics record for each metric
                record = ExtractedKeyMetrics(
                    case_id=case.id,
                    name=metric['name'],
                    description=metric['infoLines'][0] if metric['infoLines'] else f"{metric['name']} financial data",
                    data=metric['dataPoints']  # Store data points as JSONB
                )
                metric_records.append(record)
            
            # Insert all records
            for record in metric_records:
                session.add(record)
            
            await session.commit()
            print(f"Successfully seeded {len(metric_records)} individual extracted key metrics records!")
            
            # Verify insertion
            result = await session.execute(
                select(ExtractedKeyMetrics).where(ExtractedKeyMetrics.case_id == case.id)
            )
            saved_records = result.scalars().all()
            
            print("\nSeeded extracted key metrics records:")
            for record in saved_records:
                print(f"  - ID {record.id}: {record.name}")
                print(f"    Description: {record.description}")
                print(f"    Data points: {len(record.data)} months")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding extracted key metrics: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed extracted_key_metrics table with individual records...")
    await seed_extracted_key_metrics_individual()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
