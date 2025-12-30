from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from emergentintegrations.llm.chat import LlmChat, UserMessage
import asyncio


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# JWT Configuration
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 1 week

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# LLM Configuration
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')

# ==================== MODELS ====================

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None
    role: str  # "user" or "technician"
    passwordHash: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class Technician(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    verifiedStatus: bool = False
    categories: List[str] = []  # ["plumbing", "electrical", "appliance"]
    skills: str = ""
    serviceAreas: List[str] = []  # districts
    ratingAverage: float = 0.0
    reviewsCount: int = 0
    basePricingInfo: str = ""
    availabilitySlots: List[str] = []  # ["2025-01-20T09:00", "2025-01-20T14:00"]
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class ServiceRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    category: Optional[str] = None  # final selected
    descriptionText: str
    mediaUrls: List[str] = []  # base64 images/videos
    aiSuggestedCategory: Optional[str] = None
    aiSummary: Optional[str] = None
    aiConfidence: Optional[str] = None
    location: Optional[str] = None
    urgency: str = "normal"  # "normal" or "urgent"
    status: str = "created"  # created, matched, booked, in_progress, completed
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class Booking(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    serviceRequestId: str
    technicianId: str
    scheduledTime: str
    address: str
    estimatedPrice: str
    status: str = "scheduled"  # scheduled, in_progress, completed, cancelled
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class Payment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    bookingId: str
    amount: float
    status: str = "held"  # held, released, refunded
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    bookingId: str
    userId: str
    technicianId: str
    rating: int  # 1-5
    comment: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)

# ==================== REQUEST/RESPONSE MODELS ====================

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role: str  # "user" or "technician"
    address: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str
    user: dict

class CreateServiceRequestInput(BaseModel):
    descriptionText: str
    mediaUrls: List[str] = []
    urgency: str = "normal"
    location: Optional[str] = None

class AIAnalysisResponse(BaseModel):
    category: str
    summary: str
    confidence: str

class TechnicianProfileInput(BaseModel):
    categories: List[str]
    skills: str
    serviceAreas: List[str]
    basePricingInfo: str
    availabilitySlots: List[str]

class CreateBookingInput(BaseModel):
    serviceRequestId: str
    technicianId: str
    scheduledTime: str
    address: str
    estimatedPrice: str

class CreateReviewInput(BaseModel):
    bookingId: str
    technicianId: str
    rating: int
    comment: str

class UpdateStatusInput(BaseModel):
    status: str

# ==================== HELPER FUNCTIONS ====================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = decode_token(token)
    user = await db.users.find_one({"id": payload.get("sub")})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

async def analyze_with_ai(description: str) -> dict:
    """Analyze service request using LLM"""
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=str(uuid.uuid4()),
            system_message="You are a home repair classification assistant. Analyze the problem description and return ONLY a valid JSON object with these exact fields: category (one of: plumbing, electrical, appliance, other), summary (1-2 sentences in simple language), confidence (one of: low, medium, high). Do not include any other text or explanation."
        ).with_model("openai", "gpt-5.2")
        
        user_message = UserMessage(
            text=f"Classify this home repair problem: {description}"
        )
        
        response = await chat.send_message(user_message)
        
        # Parse the response
        import json
        result = json.loads(response)
        
        return {
            "category": result.get("category", "other"),
            "summary": result.get("summary", description[:100]),
            "confidence": result.get("confidence", "medium")
        }
    except Exception as e:
        logger.error(f"AI analysis error: {e}")
        # Fallback to rule-based
        return rule_based_classification(description)

def rule_based_classification(description: str) -> dict:
    """Fallback rule-based classification"""
    description_lower = description.lower()
    
    # Keywords for categories
    plumbing_keywords = ["leak", "pipe", "water", "drain", "toilet", "sink", "faucet", "plumbing"]
    electrical_keywords = ["electric", "power", "outlet", "switch", "light", "wire", "circuit"]
    appliance_keywords = ["refrigerator", "washing machine", "dryer", "dishwasher", "oven", "appliance"]
    
    category = "other"
    confidence = "low"
    
    if any(keyword in description_lower for keyword in plumbing_keywords):
        category = "plumbing"
        confidence = "medium"
    elif any(keyword in description_lower for keyword in electrical_keywords):
        category = "electrical"
        confidence = "medium"
    elif any(keyword in description_lower for keyword in appliance_keywords):
        category = "appliance"
        confidence = "medium"
    
    summary = description[:100] + "..." if len(description) > 100 else description
    
    return {
        "category": category,
        "summary": summary,
        "confidence": confidence
    }

def calculate_technician_rank(technician: dict, category: str, location: str) -> float:
    """Calculate ranking score for technician matching"""
    score = 0.0
    
    # Rating (40%)
    score += technician.get("ratingAverage", 0) * 0.4
    
    # Category match (30%)
    if category in technician.get("categories", []):
        score += 3.0 * 0.3
    
    # Service area match (20%) - simplified for MVP
    if location and location in technician.get("serviceAreas", []):
        score += 5.0 * 0.2
    
    # Availability (10%) - has slots available
    if len(technician.get("availabilitySlots", [])) > 0:
        score += 5.0 * 0.1
    
    return score

# ==================== ROUTES ====================

@api_router.get("/")
async def root():
    return {"message": "AppliFix API - Home Repair Service Platform", "status": "active"}

@api_router.post("/auth/register", response_model=LoginResponse)
async def register(input: RegisterRequest):
    # Check if user exists
    existing_user = await db.users.find_one({"email": input.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        name=input.name,
        email=input.email,
        phone=input.phone,
        address=input.address,
        role=input.role,
        passwordHash=hash_password(input.password)
    )
    
    await db.users.insert_one(user.dict())
    
    # If technician, create technician profile
    if input.role == "technician":
        technician = Technician(userId=user.id)
        await db.technicians.insert_one(technician.dict())
    
    # Create token
    token = create_access_token({"sub": user.id, "role": user.role})
    
    return LoginResponse(
        token=token,
        user={
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "address": user.address
        }
    )

@api_router.post("/auth/login", response_model=LoginResponse)
async def login(input: LoginRequest):
    user = await db.users.find_one({"email": input.email})
    if not user or not verify_password(input.password, user["passwordHash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user["id"], "role": user["role"]})
    
    return LoginResponse(
        token=token,
        user={
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "phone": user["phone"],
            "role": user["role"],
            "address": user.get("address")
        }
    )

@api_router.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "name": current_user["name"],
        "email": current_user["email"],
        "phone": current_user["phone"],
        "role": current_user["role"],
        "address": current_user.get("address")
    }

@api_router.post("/service-requests", response_model=ServiceRequest)
async def create_service_request(input: CreateServiceRequestInput, current_user: dict = Depends(get_current_user)):
    # Analyze with AI
    ai_result = await analyze_with_ai(input.descriptionText)
    
    service_request = ServiceRequest(
        userId=current_user["id"],
        descriptionText=input.descriptionText,
        mediaUrls=input.mediaUrls,
        urgency=input.urgency,
        location=input.location or current_user.get("address"),
        aiSuggestedCategory=ai_result["category"],
        aiSummary=ai_result["summary"],
        aiConfidence=ai_result["confidence"],
        category=ai_result["category"]  # Auto-set based on AI
    )
    
    await db.service_requests.insert_one(service_request.dict())
    return service_request

@api_router.get("/service-requests/{request_id}")
async def get_service_request(request_id: str, current_user: dict = Depends(get_current_user)):
    service_request = await db.service_requests.find_one({"id": request_id})
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    return service_request

@api_router.get("/service-requests")
async def get_user_service_requests(current_user: dict = Depends(get_current_user)):
    requests = await db.service_requests.find({"userId": current_user["id"]}).to_list(100)
    return requests

@api_router.get("/service-requests/{request_id}/matches")
async def get_technician_matches(request_id: str, current_user: dict = Depends(get_current_user)):
    service_request = await db.service_requests.find_one({"id": request_id})
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    category = service_request.get("category")
    location = service_request.get("location")
    
    # Get all technicians
    all_technicians = await db.technicians.find().to_list(100)
    
    # Rank technicians
    ranked_technicians = []
    for tech in all_technicians:
        score = calculate_technician_rank(tech, category, location)
        tech["matchScore"] = score
        
        # Get user info
        user = await db.users.find_one({"id": tech["userId"]})
        if user:
            tech["name"] = user["name"]
            tech["phone"] = user["phone"]
        
        ranked_technicians.append(tech)
    
    # Sort by score descending
    ranked_technicians.sort(key=lambda x: x["matchScore"], reverse=True)
    
    return ranked_technicians

@api_router.get("/technicians/{technician_id}")
async def get_technician(technician_id: str):
    technician = await db.technicians.find_one({"id": technician_id})
    if not technician:
        raise HTTPException(status_code=404, detail="Technician not found")
    
    # Get user info
    user = await db.users.find_one({"id": technician["userId"]})
    if user:
        technician["name"] = user["name"]
        technician["phone"] = user["phone"]
    
    # Get reviews
    reviews = await db.reviews.find({"technicianId": technician_id}).to_list(50)
    technician["reviews"] = reviews
    
    return technician

@api_router.put("/technicians/profile")
async def update_technician_profile(input: TechnicianProfileInput, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "technician":
        raise HTTPException(status_code=403, detail="Only technicians can update profile")
    
    technician = await db.technicians.find_one({"userId": current_user["id"]})
    if not technician:
        raise HTTPException(status_code=404, detail="Technician profile not found")
    
    update_data = {
        "categories": input.categories,
        "skills": input.skills,
        "serviceAreas": input.serviceAreas,
        "basePricingInfo": input.basePricingInfo,
        "availabilitySlots": input.availabilitySlots,
        "verifiedStatus": True  # Mock verification
    }
    
    await db.technicians.update_one(
        {"userId": current_user["id"]},
        {"$set": update_data}
    )
    
    return {"message": "Profile updated successfully"}

@api_router.post("/bookings", response_model=Booking)
async def create_booking(input: CreateBookingInput, current_user: dict = Depends(get_current_user)):
    booking = Booking(
        serviceRequestId=input.serviceRequestId,
        technicianId=input.technicianId,
        scheduledTime=input.scheduledTime,
        address=input.address,
        estimatedPrice=input.estimatedPrice
    )
    
    await db.bookings.insert_one(booking.dict())
    
    # Update service request status
    await db.service_requests.update_one(
        {"id": input.serviceRequestId},
        {"$set": {"status": "booked"}}
    )
    
    # Create mock payment
    payment = Payment(
        bookingId=booking.id,
        amount=float(input.estimatedPrice.replace("$", "").replace(",", ""))
    )
    await db.payments.insert_one(payment.dict())
    
    return booking

@api_router.get("/bookings")
async def get_user_bookings(current_user: dict = Depends(get_current_user)):
    if current_user["role"] == "user":
        # Get user's bookings via service requests
        service_requests = await db.service_requests.find({"userId": current_user["id"]}).to_list(100)
        request_ids = [sr["id"] for sr in service_requests]
        bookings = await db.bookings.find({"serviceRequestId": {"$in": request_ids}}).to_list(100)
    else:
        # Get technician's bookings
        technician = await db.technicians.find_one({"userId": current_user["id"]})
        if technician:
            bookings = await db.bookings.find({"technicianId": technician["id"]}).to_list(100)
        else:
            bookings = []
    
    # Enrich with additional data
    for booking in bookings:
        service_request = await db.service_requests.find_one({"id": booking["serviceRequestId"]})
        if service_request:
            booking["serviceRequest"] = service_request
        
        technician = await db.technicians.find_one({"id": booking["technicianId"]})
        if technician:
            user = await db.users.find_one({"id": technician["userId"]})
            if user:
                booking["technicianName"] = user["name"]
    
    return bookings

@api_router.get("/bookings/{booking_id}")
async def get_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    booking = await db.bookings.find_one({"id": booking_id})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Enrich with service request
    service_request = await db.service_requests.find_one({"id": booking["serviceRequestId"]})
    if service_request:
        booking["serviceRequest"] = service_request
    
    # Enrich with technician info
    technician = await db.technicians.find_one({"id": booking["technicianId"]})
    if technician:
        user = await db.users.find_one({"id": technician["userId"]})
        if user:
            booking["technicianName"] = user["name"]
            booking["technicianPhone"] = user["phone"]
    
    return booking

@api_router.put("/bookings/{booking_id}/status")
async def update_booking_status(booking_id: str, input: UpdateStatusInput, current_user: dict = Depends(get_current_user)):
    booking = await db.bookings.find_one({"id": booking_id})
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    await db.bookings.update_one(
        {"id": booking_id},
        {"$set": {"status": input.status}}
    )
    
    # Update service request status accordingly
    status_map = {
        "in_progress": "in_progress",
        "completed": "completed",
        "cancelled": "created"
    }
    
    if input.status in status_map:
        await db.service_requests.update_one(
            {"id": booking["serviceRequestId"]},
            {"$set": {"status": status_map[input.status]}}
        )
    
    # If completed, release payment
    if input.status == "completed":
        await db.payments.update_one(
            {"bookingId": booking_id},
            {"$set": {"status": "released"}}
        )
    
    return {"message": "Status updated successfully"}

@api_router.get("/technician/jobs")
async def get_technician_jobs(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "technician":
        raise HTTPException(status_code=403, detail="Only technicians can access this")
    
    technician = await db.technicians.find_one({"userId": current_user["id"]})
    if not technician:
        raise HTTPException(status_code=404, detail="Technician profile not found")
    
    # Get all service requests matching technician's categories
    categories = technician.get("categories", [])
    service_requests = await db.service_requests.find({
        "category": {"$in": categories},
        "status": "created"
    }).to_list(100)
    
    return service_requests

@api_router.post("/reviews", response_model=Review)
async def create_review(input: CreateReviewInput, current_user: dict = Depends(get_current_user)):
    # Verify booking is completed
    booking = await db.bookings.find_one({"id": input.bookingId})
    if not booking or booking["status"] != "completed":
        raise HTTPException(status_code=400, detail="Can only review completed bookings")
    
    review = Review(
        bookingId=input.bookingId,
        userId=current_user["id"],
        technicianId=input.technicianId,
        rating=input.rating,
        comment=input.comment
    )
    
    await db.reviews.insert_one(review.dict())
    
    # Update technician rating
    all_reviews = await db.reviews.find({"technicianId": input.technicianId}).to_list(1000)
    avg_rating = sum(r["rating"] for r in all_reviews) / len(all_reviews)
    
    await db.technicians.update_one(
        {"id": input.technicianId},
        {"$set": {
            "ratingAverage": round(avg_rating, 2),
            "reviewsCount": len(all_reviews)
        }}
    )
    
    return review

@api_router.get("/reviews/technician/{technician_id}")
async def get_technician_reviews(technician_id: str):
    reviews = await db.reviews.find({"technicianId": technician_id}).to_list(100)
    
    # Enrich with user names
    for review in reviews:
        user = await db.users.find_one({"id": review["userId"]})
        if user:
            review["userName"] = user["name"]
    
    return reviews

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
