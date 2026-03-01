"""
Seed script to populate datasimulator_benefits table with data simulator benefits data
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.datasimulator_benefits import DatasimulatorBenefits
from app.models.case import Case


async def seed_datasimulator_benefits():
    """Seed the datasimulator_benefits table with data simulator benefits data"""
    
    # Data structure based on user input
    datasimulator_benefits_data = {
        "offerings": ["AI-Powered Document Processing", "Real-time Covenant Monitoring", "Automated Compliance Checks"],
        "speed": {
            "title": "Before/After Impact Timeline",
            "earlier": {
                "label": "Earlier (Without AI Integration)",
                "value": "3 Days"
            },
            "now": {
                "label": "Now (with AI)",
                "value": "30 Minutes"
            }
        },
        "accuracy": {
            "title": "Accuracy (OCR/NLP Error Reduction Metrics)",
            "metrics": [
                {
                    "title": "Faster Covenant Checks",
                    "items": [
                        "Global Logistics Provider secured 65% faster Covenant Checks.",
                        "XYZ Company secured 35% faster Covenant Checks."
                    ]
                },
                {
                    "title": "Fewer Errors",
                    "items": [
                        "Global Logistics Provider, reduced 40% error in processing.",
                        "XYZ Company, reduced 40% error in processing."
                    ]
                }
            ]
        },
        "compliance": {
            "title": "Compliance",
            "proactiveAlerts": [
                {
                    "category": "Transport Incident",
                    "company": "XYZ Holdings (Offshore)",
                    "description": "Temporal Routing Path Rerouted through unknown server node (Hong Kong)"
                },
                {
                    "category": "Biometrics Mold Data",
                    "description": "Mismatch - Integrity violated"
                }
            ],
            "missedBreaches": [
                {
                    "type": "Covenant Breach",
                    "label": "DEBT RATIO EXCEEDED"
                },
                {
                    "type": "Reporting Deadline",
                    "label": "MISSED BY 3 DAYS"
                },
                {
                    "type": "Document Verification",
                    "label": "INCOMPLETE"
                }
            ]
        }
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
            
            # Check if datasimulator benefits already exist for this case
            result = await session.execute(
                select(DatasimulatorBenefits).where(DatasimulatorBenefits.case_id == case.id)
            )
            existing_record = result.scalars().first()
            
            if existing_record:
                print(f"Found existing datasimulator benefits record for this case. Updating with new data.")
                existing_record.data = datasimulator_benefits_data
            else:
                print(f"Creating new datasimulator benefits record.")
                datasimulator_benefits = DatasimulatorBenefits(
                    case_id=case.id,
                    data=datasimulator_benefits_data
                )
                session.add(datasimulator_benefits)
            
            await session.commit()
            print(f"Successfully seeded datasimulator benefits data!")
            
            # Verify insertion
            result = await session.execute(
                select(DatasimulatorBenefits).where(DatasimulatorBenefits.case_id == case.id)
            )
            saved_record = result.scalars().first()
            
            if saved_record:
                print(f"\nSaved datasimulator benefits data:")
                print(f"  - Case ID: {saved_record.case_id}")
                print(f"  - Offerings: {len(saved_record.data.get('offerings', []))} items")
                print(f"  - Speed: {saved_record.data.get('speed', {}).get('title', 'N/A')}")
                print(f"    * Earlier: {saved_record.data.get('speed', {}).get('earlier', {}).get('value', 'N/A')}")
                print(f"    * Now: {saved_record.data.get('speed', {}).get('now', {}).get('value', 'N/A')}")
                print(f"  - Accuracy Metrics: {len(saved_record.data.get('accuracy', {}).get('metrics', []))} items")
                print(f"  - Compliance:")
                print(f"    * Proactive Alerts: {len(saved_record.data.get('compliance', {}).get('proactiveAlerts', []))} items")
                print(f"    * Missed Breaches: {len(saved_record.data.get('compliance', {}).get('missedBreaches', []))} items")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding datasimulator benefits: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed datasimulator_benefits table...")
    await seed_datasimulator_benefits()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
