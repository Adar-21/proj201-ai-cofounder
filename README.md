# AppliFix - Home Repair Service Platform MVP

A mobile-first platform connecting homeowners with trusted home repair professionals in Istanbul.

## 🎯 Features

- **Dual Role System**: Users and Technicians with separate flows
- **AI-Powered Classification**: OpenAI GPT-5.2 categorizes repair issues (plumbing, electrical, appliance)
- **Smart Matching**: Ranked technician recommendations based on ratings, location, and availability
- **Secure Booking**: Escrow-style mock payment system
- **Real-time Updates**: Track service requests and bookings

## 🛠 Tech Stack

- **Frontend**: React Native (Expo)
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **AI**: OpenAI GPT-5.2 via Emergent LLM Key

## 📋 Prerequisites

- Node.js 18+ and yarn
- Python 3.11+
- MongoDB running on localhost:27017

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file (see .env.example)
cp .env.example .env

# Seed the database with test data
python seed_data.py

# Start the server
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

Backend will run on: `http://localhost:8001`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
yarn install

# Create .env file (see .env.example)
cp .env.example .env

# Start Expo
yarn start
```

Frontend will run on: `http://localhost:3000`

## 🔑 Test Credentials

**User Account:**
- Email: `ecem@test.com`
- Password: `password123`

**Technician Account:**
- Email: `mehmet@tech.com`
- Password: `password123`

## 📱 Demo Flow (2 minutes)

### As a User:

1. **Login** with `ecem@test.com` / `password123`
2. **Create Request**: Tap "Create New Request"
   - Enter: "My kitchen sink is leaking badly"
   - Submit
3. **View AI Analysis**: See AI categorization as "Plumbing" with confidence level
4. **Find Technicians**: Tap "Find Technicians"
   - View ranked list with match scores (60-70%)
5. **Book Appointment**: 
   - Select technician (e.g., Mehmet Demir)
   - Choose available time slot
   - Tap "Book Appointment"
   - Confirm mock payment (amount shown)
   - See success confirmation
6. **View Requests**: Go to "Requests" tab to see all your service requests

### As a Technician:

1. **Login** with `mehmet@tech.com` / `password123`
2. **View Jobs**: See available service requests matching your skills
3. **Accept/Manage**: View job details and availability

## 📁 Project Structure

```
/app
├── backend/
│   ├── server.py          # FastAPI application
│   ├── seed_data.py       # Database seeding script
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Backend configuration
├── frontend/
│   ├── app/              # Expo Router file-based routing
│   │   ├── (tabs)/       # Tab navigation screens
│   │   ├── auth/         # Login/Register screens
│   │   ├── user/         # User-specific screens
│   │   ├── technician/   # Technician-specific screens
│   │   ├── contexts/     # React Context (Auth)
│   │   └── utils/        # API utilities
│   ├── package.json
│   └── .env              # Frontend configuration
├── README.md
├── GETTING_STARTED.md
└── DEMO_SCRIPT.md
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Service Requests
- `POST /api/service-requests` - Create request (includes AI classification)
- `GET /api/service-requests` - Get user's requests
- `GET /api/service-requests/{id}` - Get request details
- `GET /api/service-requests/{id}/matches` - Get ranked technicians

### Bookings
- `POST /api/bookings` - Create booking (includes mock payment)
- `GET /api/bookings` - Get user/technician bookings
- `GET /api/bookings/{id}` - Get booking details

### Technicians
- `GET /api/technicians/{id}` - Get technician profile
- `PUT /api/technicians/profile` - Update technician profile
- `GET /api/technician/jobs` - Get available jobs

## 💳 Mock Payment System

- Payment status: `held` (escrow) → `released` (on completion)
- No real payment processing
- Amounts are estimated based on technician pricing

## 🧪 Testing

The application has been tested for:
- ✅ User authentication (login/register)
- ✅ Service request creation with photo upload
- ✅ AI categorization (OpenAI GPT-5.2)
- ✅ Technician matching and ranking
- ✅ Complete booking flow
- ✅ Mock escrow payment
- ✅ Request persistence across sessions

## 📝 Environment Variables

See `.env.example` files in both `backend/` and `frontend/` directories.

## 🐛 Known Limitations (MVP)

- Payment is mocked (no real payment gateway)
- Technician verification is auto-approved
- Location matching is simplified
- Image uploads stored as base64 (not recommended for production)

## 🚢 Deployment Notes

- Backend: Deploy FastAPI app with MongoDB connection
- Frontend: Use Expo EAS Build for mobile app deployment
- Environment variables must be configured for production

## 📄 License

MIT

## 👥 Support

For issues or questions, contact the development team.

---

**Version**: 1.0.0 (MVP)  
**Last Updated**: December 2025
