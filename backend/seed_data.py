import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_database():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Clearing existing data...")
    await db.users.delete_many({})
    await db.technicians.delete_many({})
    await db.service_requests.delete_many({})
    await db.bookings.delete_many({})
    await db.payments.delete_many({})
    await db.reviews.delete_many({})
    
    print("Creating seed data...")
    
    # Create test user
    test_user = {
        "id": "user-001",
        "name": "Ecem Yılmaz",
        "email": "ecem@test.com",
        "phone": "+90 555 123 4567",
        "address": "Kadıköy, Istanbul",
        "role": "user",
        "passwordHash": pwd_context.hash("password123"),
        "createdAt": "2025-01-01T10:00:00"
    }
    await db.users.insert_one(test_user)
    print(f"✓ Created user: {test_user['email']}")
    
    # Create test technicians
    technicians_data = [
        {
            "userId": "tech-001",
            "name": "Mehmet Demir",
            "email": "mehmet@tech.com",
            "phone": "+90 555 234 5678",
            "categories": ["plumbing", "electrical"],
            "skills": "10 years experience in plumbing and electrical repairs",
            "serviceAreas": ["Kadıköy", "Üsküdar", "Beşiktaş"],
            "ratingAverage": 4.8,
            "reviewsCount": 45,
            "basePricingInfo": "$50-150 depending on job complexity",
            "availabilitySlots": ["2025-01-20T09:00", "2025-01-20T14:00", "2025-01-21T10:00"],
            "verifiedStatus": True
        },
        {
            "userId": "tech-002",
            "name": "Ali Kara",
            "email": "ali@tech.com",
            "phone": "+90 555 345 6789",
            "categories": ["appliance"],
            "skills": "Specialist in refrigerator and washing machine repairs",
            "serviceAreas": ["Kadıköy", "Moda", "Fenerbahçe"],
            "ratingAverage": 4.6,
            "reviewsCount": 38,
            "basePricingInfo": "$40-120",
            "availabilitySlots": ["2025-01-20T11:00", "2025-01-21T09:00", "2025-01-22T14:00"],
            "verifiedStatus": True
        },
        {
            "userId": "tech-003",
            "name": "Ayşe Şahin",
            "email": "ayse@tech.com",
            "phone": "+90 555 456 7890",
            "categories": ["electrical", "appliance"],
            "skills": "Certified electrician with appliance repair expertise",
            "serviceAreas": ["Kadıköy", "Acıbadem", "Kozyatağı"],
            "ratingAverage": 4.9,
            "reviewsCount": 62,
            "basePricingInfo": "$60-180",
            "availabilitySlots": ["2025-01-20T10:00", "2025-01-20T15:00", "2025-01-21T11:00"],
            "verifiedStatus": True
        },
    ]
    
    for tech_data in technicians_data:
        # Create user account for technician
        tech_user = {
            "id": tech_data["userId"],
            "name": tech_data["name"],
            "email": tech_data["email"],
            "phone": tech_data["phone"],
            "role": "technician",
            "passwordHash": pwd_context.hash("password123"),
            "createdAt": "2025-01-01T10:00:00"
        }
        await db.users.insert_one(tech_user)
        
        # Create technician profile
        tech_profile = {
            "id": f"techprofile-{tech_data['userId']}",
            "userId": tech_data["userId"],
            "verifiedStatus": tech_data["verifiedStatus"],
            "categories": tech_data["categories"],
            "skills": tech_data["skills"],
            "serviceAreas": tech_data["serviceAreas"],
            "ratingAverage": tech_data["ratingAverage"],
            "reviewsCount": tech_data["reviewsCount"],
            "basePricingInfo": tech_data["basePricingInfo"],
            "availabilitySlots": tech_data["availabilitySlots"],
            "createdAt": "2025-01-01T10:00:00"
        }
        await db.technicians.insert_one(tech_profile)
        print(f"✓ Created technician: {tech_data['email']}")
    
    print("\n✅ Seed data created successfully!")
    print("\nTest Credentials:")
    print("User Account: ecem@test.com / password123")
    print("Technician Accounts: mehmet@tech.com / password123")
    print("                     ali@tech.com / password123")
    print("                     ayse@tech.com / password123")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
