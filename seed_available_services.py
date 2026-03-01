"""
Seed script to populate available_services table with initial data
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal, engine
from app.models.available_service import AvailableService


async def seed_available_services():
    """Seed the available_services table with initial data"""
    
    services_data = [
        {
            "name": "Loan Agreement",
            "description": "Manage and track loan agreements, terms, and conditions"
        },
        {
            "name": "Covenant Register",
            "description": "Monitor and manage loan covenants and compliance requirements"
        },
        {
            "name": "FR Y-14 Reporting",
            "description": "Federal Reserve Y-14 regulatory reporting and submissions"
        },
        {
            "name": "Financials & ESG Reports",
            "description": "Financial statements and Environmental, Social, and Governance reports"
        },
        {
            "name": "KYC/AML file",
            "description": "Know Your Customer and Anti-Money Laundering documentation and verification"
        },
        {
            "name": "Risk Dashboard",
            "description": "Comprehensive risk monitoring and analytics dashboard"
        },
        {
            "name": "Client Communication",
            "description": "Client communication portal and messaging system"
        },
        {
            "name": "Blockchain ledger",
            "description": "Distributed ledger technology for transaction tracking and verification"
        }
    ]
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if services already exist
            result = await session.execute(select(AvailableService))
            existing_services = result.scalars().all()
            
            if existing_services:
                print(f"Found {len(existing_services)} existing services. Skipping seed.")
                return
            
            # Insert new services
            for service_data in services_data:
                service = AvailableService(**service_data)
                session.add(service)
            
            await session.commit()
            print(f"Successfully seeded {len(services_data)} services!")
            
            # Verify insertion
            result = await session.execute(select(AvailableService))
            all_services = result.scalars().all()
            
            print("\nSeeded services:")
            for service in all_services:
                print(f"  - {service.id}: {service.name}")
                
        except Exception as e:
            await session.rollback()
            print(f"Error seeding services: {e}")
            raise


async def main():
    """Main function to run the seed script"""
    print("Starting to seed available_services table...")
    await seed_available_services()
    print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(main())
