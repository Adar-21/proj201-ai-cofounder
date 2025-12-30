# AppliFix MVP - Demo Script (Under 2 Minutes)

## Demo Flow: User Journey

### Setup (30 seconds)
**Narrator:** "AppliFix connects Istanbul residents with trusted home repair professionals. Let's see how Ecem, a 29-year-old marketing professional, uses it."

**Show:** Launch app, display onboarding/login screen

---

### Act 1: Problem Discovery (20 seconds)
**Narrator:** "Ecem comes home to find her kitchen sink leaking. Instead of calling random plumbers, she opens AppliFix."

**Actions:**
1. Login as ecem@test.com
2. Tap "Create New Request" button
3. Upload photo of leaking sink
4. Type: "Kitchen sink is leaking under the basin, water dripping constantly"
5. Select urgency: "Urgent"
6. Tap "Submit Request"

---

### Act 2: AI Magic (15 seconds)
**Narrator:** "AppliFix's AI analyzes the problem instantly."

**Show:**
- AI Result Screen displays:
  - **Category:** PLUMBING
  - **Summary:** "Leaking kitchen sink under basin requiring immediate plumbing attention"
  - **Confidence:** HIGH
  - Disclaimer visible

**Narrator:** "High confidence - it's clearly a plumbing issue."

---

### Act 3: Finding the Right Pro (25 seconds)
**Narrator:** "Now she browses verified technicians, ranked by ratings, distance, and availability."

**Actions:**
1. Tap "Find Technicians"
2. Show list of ranked technicians:
   - **Ayşe Şahin** - 4.9★ (62 reviews) - Match 95%
   - **Mehmet Demir** - 4.8★ (45 reviews) - Match 88%
   - **Ali Kara** - 4.6★ (38 reviews) - Match 75%
3. Tap on Ayşe Şahin

---

### Act 4: Profile & Booking (20 seconds)
**Narrator:** "Ecem checks Ayşe's profile - verified, experienced, great reviews."

**Show:**
- ✓ Verified badge
- Specialties: Electrical, Appliance
- $60-180 pricing
- Service areas: Kadıköy ✓
- Available slots visible

**Actions:**
1. Select time slot: "Tomorrow, 10:00 AM"
2. Tap "Book Appointment"

---

### Act 5: Secure Payment (10 seconds)
**Narrator:** "Funds are held securely in escrow until the job is complete."

**Show:**
- Booking confirmed screen
- Payment status: "Funds Held"
- Technician notified

---

### Act 6: Tracking & Completion (15 seconds)
**Narrator:** "Ecem tracks the job status in real-time."

**Show:**
- Requests tab
- Status progression:
  - ✓ Requested
  - ✓ Booked
  - → In Progress
  - → Completed

**Narrator:** "Once Ayşe fixes the sink, Ecem leaves a 5-star review. Problem solved!"

---

### Closing (15 seconds)
**Narrator:** "AppliFix - Finding trusted home repair professionals, made simple. AI-powered matching, verified technicians, secure payments."

**Show:**
- Quick montage of:
  - User creating request
  - AI categorizing
  - Technician accepting job
  - Payment released
  - 5-star review

**End Screen:** "AppliFix - Your Home Repair Solution"

---

## Total Time: ~2 minutes

## Test Credentials for Live Demo

### User Account
- Email: ecem@test.com
- Password: password123

### Technician Accounts (for showing other perspective)
- mehmet@tech.com / password123
- ali@tech.com / password123
- ayse@tech.com / password123

---

## Key Messages

1. **Problem Solved:** No more calling random technicians
2. **AI-Powered:** Smart categorization helps find the right expert
3. **Verified Pros:** Only background-checked technicians
4. **Transparent Pricing:** See estimates upfront
5. **Secure Payment:** Escrow-style protection
6. **Rated & Reviewed:** Community-driven quality

---

## Technical Highlights (for technical audience)

- **Cross-platform:** Single React Native codebase
- **AI Integration:** OpenAI GPT-5.2 for categorization
- **Smart Matching:** Multi-factor ranking algorithm
- **Secure Auth:** JWT with bcrypt password hashing
- **Real-time Ready:** Architecture supports WebSocket integration
- **MVP Focus:** Built in days, not months

---

## Demo Tips

1. **Pre-load data:** Run seed script before demo
2. **Have photos ready:** Use pre-prepared repair images
3. **Test flow first:** Run through once before presenting
4. **Show both sides:** Quick switch to technician view for impact
5. **Emphasize speed:** "From problem to booked in under 2 minutes"

---

## Q&A Preparation

**Q: Is the AI always accurate?**
A: We show confidence levels and always include a disclaimer. Final diagnosis is by the professional.

**Q: How do you verify technicians?**
A: MVP uses mock verification. Production would include background checks, license verification, and insurance.

**Q: What about payments?**
A: MVP simulates escrow. Production would integrate Stripe or a Turkish payment gateway.

**Q: Why Istanbul?**
A: It's our beachhead market - large urban population, common rental housing, established service economy.

**Q: What's next?**
A: Real payment integration, push notifications, in-app chat, and expanding to other Turkish cities.
