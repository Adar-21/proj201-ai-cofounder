# AppliFix - Home Repair Service Platform

## 🏠 Overview

AppliFix is a mobile MVP that connects Istanbul residents with trusted home repair professionals. The platform allows users to submit repair requests with AI-assisted categorization and book verified technicians.

### Target Market
- **Location:** Istanbul, Turkey
- **Users:** 25-40 year old full-time working renters
- **Pain Point:** Finding trusted, fairly priced home repair professionals quickly

## ✨ Key Features

### For Users:
1. **Create Service Requests** - Upload photos/videos and describe issues
2. **AI-Assisted Categorization** - Get smart suggestions for problem type
3. **Browse Verified Technicians** - View ratings, skills, and pricing
4. **Book Appointments** - Select time slots and confirm bookings
5. **Mock Escrow Payment** - Secure payment simulation
6. **Track Job Status** - Monitor repair progress
7. **Leave Reviews** - Rate technicians after completion

### For Technicians:
1. **Profile Setup** - Add skills, service areas, and availability
2. **View Job Feed** - See matching repair requests
3. **Manage Bookings** - Accept jobs and update status
4. **View Reviews** - Track customer feedback

## 🛠 Tech Stack

### Frontend
- **Framework:** Expo / React Native
- **Navigation:** Expo Router (file-based routing)
- **State Management:** React Context API
- **HTTP Client:** Axios
- **UI Icons:** @expo/vector-icons
- **Date Handling:** date-fns
- **Image Picker:** expo-image-picker
- **Storage:** @react-native-async-storage/async-storage

### Backend
- **Framework:** FastAPI (Python)
- **Database:** MongoDB (Motor async driver)
- **Authentication:** JWT
- **Password Hashing:** Passlib + bcrypt
- **AI Integration:** OpenAI GPT-5.2 (via Emergent LLM Key)

## 📁 Project Structure

```
/app
├── backend/
│   ├── server.py           # FastAPI application
│   ├── seed_data.py        # Database seeding script
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
│
└── frontend/
    ├── app/
    │   ├── _layout.tsx              # Root layout with auth provider
    │   ├── index.tsx                # Entry point/splash
    │   ├── contexts/
    │   │   └── AuthContext.tsx      # Authentication context
    │   ├── utils/
    │   │   └── api.ts               # Axios instance with interceptors
    │   ├── auth/
    │   │   ├── login.tsx            # Login screen
    │   │   └── register.tsx         # Registration screen
    │   ├── (tabs)/
    │   │   ├── _layout.tsx          # Bottom tab navigation
    │   │   ├── home.tsx             # Home dashboard
    │   │   ├── requests.tsx         # User requests/bookings list
    │   │   └── profile.tsx          # User profile
    │   ├── user/
    │   │   └── create-request.tsx   # Create service request
    │   ├── service-request/
    │   │   └── [id].tsx             # Service request details + AI result
    │   ├── technician-matches/
    │   │   └── [id].tsx             # Ranked technician list
    │   ├── technician/
    │   │   ├── [id].tsx             # Technician profile + booking
    │   │   ├── jobs.tsx             # Available jobs (for technicians)
    │   │   └── setup-profile.tsx   # Profile setup
    │   └── booking/
    │       └── [id].tsx             # Booking details
    ├── package.json
    └── app.json
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- MongoDB running locally
- Expo CLI

### Installation

1. **Clone and setup backend:**
```bash
cd /app/backend
pip install -r requirements.txt
python seed_data.py  # Creates test data
```

2. **Setup frontend:**
```bash
cd /app/frontend
yarn install
```

3. **Start services:**
```bash
# Backend (FastAPI)
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Frontend (Expo)
cd /app/frontend
expo start
```

## 🔐 Test Credentials

The seed script creates the following test accounts:

### User Account
- **Email:** ecem@test.com
- **Password:** password123
- **Role:** User

### Technician Accounts
- **Email:** mehmet@tech.com (Plumbing & Electrical)
- **Email:** ali@tech.com (Appliance)
- **Email:** ayse@tech.com (Electrical & Appliance)
- **Password:** password123 (all)

## 🤖 AI Integration

The app uses OpenAI GPT-5.2 for intelligent problem categorization:

- **Input:** User's text description of repair issue
- **Output:** 
  - Suggested category (plumbing/electrical/appliance/other)
  - Short summary (1-2 sentences)
  - Confidence level (low/medium/high)

**Fallback:** Rule-based keyword matching if AI fails

**Disclaimer:** All AI suggestions are marked as estimates requiring professional verification

## 💳 Payment System

Mock escrow-style payment implementation:
- Funds marked as "held" on booking
- Released to technician on job completion
- Can be refunded on cancellation
- **No real payment gateway** (MVP simulation only)

## 📊 Technician Ranking Algorithm

Technicians are ranked using a weighted score:

```python
score = (
    rating_average * 0.4 +           # 40% weight on ratings
    category_match * 0.3 +           # 30% weight on skill match
    service_area_match * 0.2 +       # 20% weight on location
    availability * 0.1               # 10% weight on availability
)
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User/Technician registration
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Service Requests
- `POST /api/service-requests` - Create request (with AI analysis)
- `GET /api/service-requests` - Get user's requests
- `GET /api/service-requests/{id}` - Get request details
- `GET /api/service-requests/{id}/matches` - Get ranked technicians

### Technicians
- `GET /api/technicians/{id}` - Get technician profile
- `PUT /api/technicians/profile` - Update profile
- `GET /api/technician/jobs` - Get available jobs

### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings` - Get user/technician bookings
- `GET /api/bookings/{id}` - Get booking details
- `PUT /api/bookings/{id}/status` - Update status

### Reviews
- `POST /api/reviews` - Submit review
- `GET /api/reviews/technician/{id}` - Get technician reviews

## 📱 Mobile App Features

### Navigation
- **Bottom Tabs:** Home, Requests, Profile
- **Stack Navigation:** Deep screens (booking, technician profile, etc.)
- **Role-Based:** Different home screens for users vs technicians

### Image Handling
- Photos stored as base64 strings in MongoDB
- Supports gallery selection via expo-image-picker
- Up to 3 photos per service request

### Offline Support
- JWT tokens cached in AsyncStorage
- User profile cached locally
- Auto-rehydration on app launch

## 🎯 MVP Scope

This is an MVP focused on core functionality:

### ✅ Included
- User & technician registration/login
- Service request creation with photos
- AI-powered categorization
- Technician browsing and booking
- Mock payment flow
- Basic review system

### ❌ Not Included (Future)
- Real payment gateway integration
- Real-time chat
- Push notifications
- Advanced search/filters
- Multi-language support
- Admin panel
- Advanced analytics

## 🐛 Known Limitations

1. **No Computer Vision:** AI only analyzes text, not images
2. **Static Availability:** Technicians manually set slots
3. **Simplified Matching:** Distance is mocked (no real GPS)
4. **Mock Payments:** No real transaction processing
5. **Basic Verification:** Technician verification is simulated

## 🔮 Future Enhancements

1. **Real-time Updates:** Socket.io for live status changes
2. **Push Notifications:** Expo Notifications for job alerts
3. **Payment Integration:** Stripe or local Turkish gateway
4. **GPS Integration:** Real distance calculation
5. **Chat System:** In-app messaging
6. **Video Calls:** For remote troubleshooting
7. **Background Checks:** Real technician verification
8. **Insurance:** Coverage for damages

## 📄 License

This is an MVP project for educational/demonstration purposes.

## 👥 Contact

For questions about this MVP, please refer to the project documentation.

---

**Built with ❤️ using Expo, FastAPI, and MongoDB**
