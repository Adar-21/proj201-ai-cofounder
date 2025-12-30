# AppliFix - Home Repair Service Platform MVP

A mobile-first platform connecting homeowners with trusted home repair professionals in Istanbul.

[![Tech Stack](https://img.shields.io/badge/Stack-React%20Native%20%2B%20FastAPI%20%2B%20MongoDB-blue)]() [![Status](https://img.shields.io/badge/Status-MVP%20Ready-success)]() [![License](https://img.shields.io/badge/License-MIT-green)]()

## 🎯 Features

- **Dual Role System**: Separate flows for Users (homeowners) and Technicians (service providers)
- **AI-Powered Classification**: OpenAI GPT-5.2 automatically categorizes repair issues (plumbing, electrical, appliance)
- **Smart Matching**: Ranked technician recommendations based on ratings, location, and availability
- **Secure Booking**: Complete booking flow with escrow-style mock payment
- **Real-time Updates**: Track service requests and bookings with status badges

## 🛠 Tech Stack

- **Frontend**: React Native (Expo Router)
- **Backend**: FastAPI (Python 3.11+)
- **Database**: MongoDB
- **AI**: OpenAI GPT-5.2 via Emergent LLM Key
- **Authentication**: JWT with dual-role support

## 📋 Prerequisites

- **Node.js** 18+ and **yarn**
- **Python** 3.11+
- **MongoDB** running on `localhost:27017`

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Adar-21/proj201-ai-cofounder.git
cd proj201-ai-cofounder
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your Emergent LLM Key
cat > .env << EOF
MONGO_URL="mongodb://localhost:27017"
DB_NAME="applifix_db"
JWT_SECRET_KEY="your-secret-key-change-in-production-mvp-applifix-2025"
EMERGENT_LLM_KEY="your-emergent-llm-key-here"
EOF

# Seed database with test data
python seed_data.py

# Start backend server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Backend URL**: `http://localhost:8001`  
**API Docs**: `http://localhost:8001/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
yarn install

# The .env file is pre-configured for local development
# No changes needed for local testing

# Start Expo
yarn start
```

**Frontend URL**: `http://localhost:3000`

### 4. Access the App

- **Web**: Open `http://localhost:3000` in your browser
- **Mobile**: Scan QR code with Expo Go app (iOS/Android)

## 🔑 Test Credentials

### User Account (Homeowner)
- **Email**: `ecem@test.com`
- **Password**: `password123`

### Technician Account
- **Email**: `mehmet@tech.com`
- **Password**: `password123`

## 📱 Demo Flow (2-Minute Walkthrough)

### As a User:

1. ✅ **Login**: Use `ecem@test.com` / `password123`
2. ✅ **Create Request**: Tap "Create New Request"
   - Enter: "My kitchen sink is leaking badly"
   - Optionally add photo
   - Select urgency: Normal or Urgent
   - Submit
3. ✅ **View AI Analysis**: See automatic categorization as "Plumbing" with confidence level
4. ✅ **Find Technicians**: Tap "Find Technicians"
   - View ranked list with match scores (e.g., 67%, 58%)
   - See ratings and pricing
5. ✅ **Book Appointment**: 
   - Select a technician (e.g., "Mehmet Demir")
   - Choose available time slot
   - Tap "Book Appointment"
   - Confirm mock payment in dialog
   - See success confirmation
6. ✅ **View Requests**: Go to "Requests" tab
   - See all your service requests
   - View status badges (Created, Booked, etc.)

### As a Technician:

1. ✅ **Login**: Use `mehmet@tech.com` / `password123`
2. ✅ **View Jobs**: See available service requests matching your skills
3. ✅ **Manage Bookings**: View accepted jobs in "Requests" tab

## 🌐 Environment Variables

### Backend (`backend/.env`)

```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="applifix_db"
JWT_SECRET_KEY="your-secret-key-change-in-production"
EMERGENT_LLM_KEY="your-emergent-llm-key"
```

**Get Emergent LLM Key**: https://emergent.ai/profile

### Frontend (`frontend/.env`)

```env
EXPO_PUBLIC_BACKEND_URL=http://localhost:8001
```

*Note: Other Expo variables are auto-configured*

## 📁 Project Structure

```
.
├── backend/
│   ├── server.py          # FastAPI application
│   ├── seed_data.py       # Database seeding script
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Backend configuration
├── frontend/
│   ├── app/              # Expo Router file-based routing
│   │   ├── (tabs)/       # Tab navigation (Home, Requests, Profile)
│   │   ├── auth/         # Login & Registration
│   │   ├── user/         # User-specific screens
│   │   ├── technician/   # Technician screens & booking
│   │   ├── contexts/     # Auth Context Provider
│   │   └── utils/        # API client
│   ├── package.json
│   └── .env
├── docs/
│   └── final_delivery.md # Complete MVP documentation
└── README.md
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - Create account (user/technician)
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Service Requests
- `POST /api/service-requests` - Create request with AI classification
- `GET /api/service-requests` - Get user's requests
- `GET /api/service-requests/{id}` - Get request details
- `GET /api/service-requests/{id}/matches` - Get ranked technicians

### Bookings
- `POST /api/bookings` - Create booking with mock payment
- `GET /api/bookings` - Get user/technician bookings
- `GET /api/bookings/{id}` - Get booking details
- `PUT /api/bookings/{id}/status` - Update booking status

### Technicians
- `GET /api/technicians/{id}` - Get technician profile
- `PUT /api/technicians/profile` - Update profile
- `GET /api/technician/jobs` - Get available jobs

## 💳 Mock Payment System

- Payment confirmation dialog before booking
- Payment status: `held` (escrow) → `released` (on completion)
- Amounts based on technician pricing
- **No real transactions processed**

## 🧪 Testing

The MVP has been tested for:

- ✅ User authentication (register/login for both roles)
- ✅ Service request creation with photo upload
- ✅ AI categorization with OpenAI GPT-5.2
- ✅ Technician matching with ranking algorithm
- ✅ Complete booking flow with time slot selection
- ✅ Mock escrow payment confirmation
- ✅ Request persistence and status tracking
- ✅ Tab navigation and screen transitions

## 🐛 Known Limitations (MVP)

- Payment is mocked (no real payment gateway)
- Technician verification is auto-approved
- Location matching is simplified (string comparison)
- Images stored as base64 (not scalable)
- No real-time notifications
- No offline mode

## 📚 Additional Documentation

- **Complete MVP Details**: See `/docs/final_delivery.md`
- **Original Requirements**: See `GETTING_STARTED.md`
- **Demo Script**: See `DEMO_SCRIPT.md`

## 🚀 Next Steps

1. User testing and feedback collection
2. Real payment gateway integration (Stripe)
3. Cloud storage for images (AWS S3)
4. Push notifications for booking updates
5. Advanced geolocation with Google Maps API
6. In-app chat between users and technicians
7. Admin dashboard for platform management

## 🤝 Contributing

This is an MVP project. For production deployment:

1. Replace mock payment with real gateway
2. Implement proper image storage
3. Add comprehensive error handling
4. Set up monitoring and logging
5. Implement rate limiting
6. Add automated tests
7. Security audit

## 📄 License

MIT License - See LICENSE file for details

## 👥 Support

For questions or issues:
- Check `/docs/final_delivery.md` for detailed documentation
- Review API documentation at `http://localhost:8001/docs`
- Contact development team

---

**AppliFix MVP v1.0.0** - Built with React Native, FastAPI, and MongoDB  
*Last Updated: December 2025*