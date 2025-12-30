# AppliFix MVP - Quick Start Guide

## \ud83d\ude80 Immediate Setup (5 Minutes)

### Prerequisites Check
```bash
# Check if services are running
sudo supervisorctl status
# Should show: backend RUNNING, expo RUNNING, mongodb RUNNING
```

### Test Backend API
```bash
curl http://localhost:8001/api/
# Expected: {"message":"AppliFix API - Home Repair Service Platform","status":"active"}
```

### Test Login
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ecem@test.com","password":"password123"}'
# Should return JWT token and user data
```

---

## \ud83d\udcf1 Mobile App Access

### Option 1: Expo Go App (Recommended for Testing)
1. Install Expo Go on your phone:
   - iOS: https://apps.apple.com/app/expo-go/id982107779
   - Android: https://play.google.com/store/apps/details?id=host.exp.exponent

2. Scan the QR code from terminal or use the tunnel URL

3. Login with test credentials

### Option 2: Web Browser (For Quick Preview)
1. Open the Expo web interface URL shown in the terminal
2. Login with test credentials

---

## \ud83d\udc65 Test Accounts

### User Account (Ecem - Looking for repairs)
```
Email: ecem@test.com
Password: password123
Role: User
Address: Kadıköy, Istanbul
```

### Technician Accounts (Service Providers)
```
1. Mehmet Demir (Plumbing & Electrical)
   Email: mehmet@tech.com
   Password: password123
   Rating: 4.8★ (45 reviews)
   
2. Ali Kara (Appliance Specialist)
   Email: ali@tech.com  
   Password: password123
   Rating: 4.6★ (38 reviews)
   
3. Ayşe Şahin (Electrical & Appliance)
   Email: ayse@tech.com
   Password: password123
   Rating: 4.9★ (62 reviews)
```

---

## \ud83d\udea6 Complete User Flow (Testing Checklist)

### \u2705 As a User (Ecem):

**1. Registration & Login**
- [ ] Open app
- [ ] Tap "Sign Up" (or Login if using test account)
- [ ] Select "I need repairs" role
- [ ] Enter credentials
- [ ] Successfully logged in → Home screen

**2. Create Service Request**
- [ ] Tap "Create New Request" button
- [ ] Describe problem: "Kitchen sink is leaking"
- [ ] Upload photo (optional)
- [ ] Select urgency: Normal or Urgent
- [ ] Submit request

**3. View AI Analysis**
- [ ] See AI categorization (e.g., "PLUMBING")
- [ ] Read AI summary
- [ ] Check confidence level
- [ ] Note disclaimer message

**4. Browse Technicians**
- [ ] Tap "Find Technicians"
- [ ] View ranked list (sorted by match score)
- [ ] See ratings, reviews, pricing
- [ ] Tap on a technician

**5. View Technician Profile**
- [ ] See verified badge
- [ ] Check specialties/categories
- [ ] Read skills & experience
- [ ] View pricing estimate
- [ ] See service areas
- [ ] Browse reviews

**6. Book Appointment**
- [ ] Select available time slot
- [ ] Review booking details
- [ ] Tap "Book Appointment"
- [ ] See confirmation message
- [ ] Payment status: "Funds Held"

**7. Track Job**
- [ ] Go to "Requests" tab
- [ ] See booking with status
- [ ] Status progression visible:
  - Created → Booked → In Progress → Completed

**8. Leave Review** (After completion)
- [ ] Open completed booking
- [ ] Tap "Leave Review"
- [ ] Rate 1-5 stars
- [ ] Write comment
- [ ] Submit review

---

### \u2705 As a Technician (Mehmet/Ali/Ayşe):

**1. Registration & Login**
- [ ] Open app
- [ ] Select "I'm a technician" role
- [ ] Enter credentials
- [ ] Successfully logged in

**2. Setup Profile**
- [ ] Tap "Setup Profile"
- [ ] Select categories (plumbing/electrical/appliance)
- [ ] Enter skills & experience
- [ ] Add service areas
- [ ] Set pricing range
- [ ] Save profile

**3. View Available Jobs**
- [ ] Tap "View Available Jobs"
- [ ] See list of requests matching your categories
- [ ] View problem descriptions
- [ ] Check urgency and location

**4. View My Bookings**
- [ ] Go to "Requests" tab (shows your jobs)
- [ ] See accepted bookings
- [ ] View job details
- [ ] See customer info

**5. Update Job Status**
- [ ] Open booking
- [ ] Update status:
  - Scheduled → In Progress
  - In Progress → Completed
- [ ] Customer notified automatically

**6. View Reviews**
- [ ] Go to Profile
- [ ] Tap "My Reviews"
- [ ] See ratings and comments
- [ ] Check overall rating average

---

## \ud83d\udca1 Testing Tips

### For AI Categorization
Try these test descriptions:
```
Plumbing: "Kitchen sink leaking under the basin"
Electrical: "Power outlet not working in bedroom"  
Appliance: "Refrigerator not cooling properly"
Urgent: "Water pipe burst, flooding bathroom!"
```

### For Photo Upload
- Use gallery images (no camera required for testing)
- Base64 encoding handled automatically
- Up to 3 photos per request

### For Booking Flow
- Technicians have pre-set availability slots
- Slots are 1-2 days in the future
- Multiple slots available per technician

---

## \ud83d\udc1b Troubleshooting

### Backend Not Responding
```bash
# Restart backend
sudo supervisorctl restart backend

# Check logs
sudo tail -f /var/log/supervisor/backend.err.log
```

### Frontend Not Loading
```bash
# Clear cache and restart
cd /app/frontend
rm -rf .expo node_modules/.cache
sudo supervisorctl restart expo

# Check logs  
sudo tail -f /var/log/supervisor/expo.out.log
```

### MongoDB Issues
```bash
# Check MongoDB is running
sudo supervisorctl status mongodb

# Reseed database
cd /app/backend
python seed_data.py
```

### "Unable to resolve module" Errors
```bash
# This usually means a dependency is missing
cd /app/frontend
yarn install

# Then restart
sudo supervisorctl restart expo
```

---

## \ud83d\udcca API Testing (Using curl)

### Get All Service Requests (Requires Auth)
```bash
TOKEN="your-jwt-token-here"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8001/api/service-requests
```

### Create Service Request
```bash
curl -X POST http://localhost:8001/api/service-requests \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "descriptionText": "Kitchen sink leaking badly",
    "urgency": "urgent",
    "mediaUrls": []
  }'
```

### Get Matched Technicians
```bash
REQUEST_ID="your-request-id"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8001/api/service-requests/$REQUEST_ID/matches
```

---

## \ud83d\udd10 Environment Variables

### Backend (.env)
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=applifix_db
JWT_SECRET_KEY=your-secret-key-change-in-production-mvp-applifix-2025
EMERGENT_LLM_KEY=sk-emergent-aF31b4c5d1dEaF8911
```

### Frontend (.env)
```
EXPO_PACKAGER_PROXY_URL=<auto-generated>
EXPO_PACKAGER_HOSTNAME=<auto-generated>
EXPO_PUBLIC_BACKEND_URL=https://techconnect-26.preview.emergentagent.com
```

**⚠️ DO NOT modify EXPO_PACKAGER_* variables - they're auto-generated!**

---

## \ud83d\udcdd Key Files Reference

### Frontend Structure
```
app/
├── _layout.tsx              # Root with AuthProvider
├── index.tsx                # Entry/splash screen  
├── contexts/
│   └── AuthContext.tsx      # Auth state management
├── utils/
│   └── api.ts               # Axios with JWT interceptor
├── auth/
│   ├── login.tsx            # Login screen
│   └── register.tsx         # Registration with role selection
├── (tabs)/
│   ├── home.tsx             # Dashboard (different for user/tech)
│   ├── requests.tsx         # Requests/bookings list
│   └── profile.tsx          # User profile
├── user/
│   └── create-request.tsx   # Create service request
├── service-request/
│   └── [id].tsx             # Request details + AI result
├── technician-matches/
│   └── [id].tsx             # Ranked technician list
└── technician/
    ├── [id].tsx             # Profile + booking
    ├── jobs.tsx             # Available jobs feed
    └── setup-profile.tsx    # Profile setup form
```

### Backend Structure
```
backend/
├── server.py              # FastAPI app with all routes
├── seed_data.py          # Database seeding script
├── requirements.txt      # Python dependencies
└── .env                  # Environment config
```

---

## \u2728 Feature Highlights

### \ud83e\udd16 AI-Powered Categorization
- Uses OpenAI GPT-5.2
- Analyzes user description
- Returns: category, summary, confidence
- Fallback to keyword matching

### \ud83c\udfaf Smart Technician Matching
Ranking algorithm:
- 40% - Rating average
- 30% - Category match
- 20% - Service area match
- 10% - Availability

### \ud83d\udd12 Security Features
- JWT authentication
- Bcrypt password hashing
- Bearer token in headers
- Role-based access control

### \ud83d\udcf8 Image Handling
- Base64 encoding
- Stored in MongoDB
- Up to 3 photos per request
- Works with expo-image-picker

---

## \ud83d\ude80 Next Steps

After testing the MVP:

1. **Deploy to Production**
   - Setup cloud MongoDB (Atlas)
   - Configure production secrets
   - Deploy backend (Heroku/Railway)
   - Build Expo app (EAS Build)

2. **Add Real Features**
   - Stripe payment integration
   - Push notifications
   - Real-time chat
   - GPS-based matching

3. **Scale**
   - Add more cities
   - More service categories
   - Admin dashboard
   - Analytics

---

## \ud83d\udc6f Support

For issues or questions:
1. Check this guide first
2. Review README.md
3. Check backend/frontend logs
4. Verify all services are running

---

**Happy Testing! \ud83c\udf89**
