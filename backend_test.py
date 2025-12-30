#!/usr/bin/env python3
"""
AppliFix Backend API Testing Suite
Tests all backend endpoints according to the test plan in test_result.md
"""

import requests
import json
import uuid
from datetime import datetime
import sys
import os

# Backend URL from frontend .env
BACKEND_URL = "https://techconnect-26.preview.emergentagent.com/api"

# Test credentials
USER_CREDENTIALS = {"email": "ecem@test.com", "password": "password123"}
TECHNICIAN_CREDENTIALS = {"email": "mehmet@tech.com", "password": "password123"}

class AppliFix_API_Tester:
    def __init__(self):
        self.user_token = None
        self.technician_token = None
        self.test_service_request_id = None
        self.test_technician_id = None
        self.test_booking_id = None
        self.results = {
            "auth": {"passed": 0, "failed": 0, "details": []},
            "service_requests": {"passed": 0, "failed": 0, "details": []},
            "technician_matching": {"passed": 0, "failed": 0, "details": []},
            "booking": {"passed": 0, "failed": 0, "details": []},
            "technician_jobs": {"passed": 0, "failed": 0, "details": []}
        }

    def log_result(self, category, test_name, passed, details=""):
        """Log test result"""
        if passed:
            self.results[category]["passed"] += 1
            status = "✅ PASS"
        else:
            self.results[category]["failed"] += 1
            status = "❌ FAIL"
        
        self.results[category]["details"].append(f"{status}: {test_name} - {details}")
        print(f"{status}: {test_name} - {details}")

    def test_auth_register_user(self):
        """Test user registration"""
        try:
            # Generate unique email for testing
            unique_email = f"testuser_{uuid.uuid4().hex[:8]}@test.com"
            
            payload = {
                "name": "Test User",
                "email": unique_email,
                "phone": "+90555123456",
                "password": "testpass123",
                "role": "user",
                "address": "Istanbul, Turkey"
            }
            
            response = requests.post(f"{BACKEND_URL}/auth/register", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if "token" in data and "user" in data:
                    self.log_result("auth", "User Registration", True, f"User registered successfully with email {unique_email}")
                    return True
                else:
                    self.log_result("auth", "User Registration", False, "Missing token or user in response")
                    return False
            else:
                self.log_result("auth", "User Registration", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("auth", "User Registration", False, f"Exception: {str(e)}")
            return False

    def test_auth_register_technician(self):
        """Test technician registration"""
        try:
            # Generate unique email for testing
            unique_email = f"testtechnician_{uuid.uuid4().hex[:8]}@test.com"
            
            payload = {
                "name": "Test Technician",
                "email": unique_email,
                "phone": "+90555654321",
                "password": "testpass123",
                "role": "technician",
                "address": "Istanbul, Turkey"
            }
            
            response = requests.post(f"{BACKEND_URL}/auth/register", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if "token" in data and "user" in data and data["user"]["role"] == "technician":
                    self.log_result("auth", "Technician Registration", True, f"Technician registered successfully with email {unique_email}")
                    return True
                else:
                    self.log_result("auth", "Technician Registration", False, "Missing token/user or incorrect role in response")
                    return False
            else:
                self.log_result("auth", "Technician Registration", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("auth", "Technician Registration", False, f"Exception: {str(e)}")
            return False

    def test_auth_login_user(self):
        """Test user login with seed data"""
        try:
            response = requests.post(f"{BACKEND_URL}/auth/login", json=USER_CREDENTIALS)
            
            if response.status_code == 200:
                data = response.json()
                if "token" in data and "user" in data:
                    self.user_token = data["token"]
                    self.log_result("auth", "User Login", True, f"User logged in successfully: {data['user']['email']}")
                    return True
                else:
                    self.log_result("auth", "User Login", False, "Missing token or user in response")
                    return False
            else:
                self.log_result("auth", "User Login", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("auth", "User Login", False, f"Exception: {str(e)}")
            return False

    def test_auth_login_technician(self):
        """Test technician login with seed data"""
        try:
            response = requests.post(f"{BACKEND_URL}/auth/login", json=TECHNICIAN_CREDENTIALS)
            
            if response.status_code == 200:
                data = response.json()
                if "token" in data and "user" in data:
                    self.technician_token = data["token"]
                    self.log_result("auth", "Technician Login", True, f"Technician logged in successfully: {data['user']['email']}")
                    return True
                else:
                    self.log_result("auth", "Technician Login", False, "Missing token or user in response")
                    return False
            else:
                self.log_result("auth", "Technician Login", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("auth", "Technician Login", False, f"Exception: {str(e)}")
            return False

    def test_service_request_creation_with_ai(self):
        """Test service request creation with AI classification"""
        if not self.user_token:
            self.log_result("service_requests", "Service Request Creation", False, "No user token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            payload = {
                "descriptionText": "My kitchen sink is leaking water constantly. The pipe under the sink seems broken.",
                "mediaUrls": [],
                "urgency": "normal",
                "location": "Kadikoy, Istanbul"
            }
            
            response = requests.post(f"{BACKEND_URL}/service-requests", json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["id", "aiSuggestedCategory", "aiSummary", "aiConfidence", "category"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_result("service_requests", "Service Request Creation", False, f"Missing fields: {missing_fields}")
                    return False
                
                # Check AI classification
                if data.get("aiSuggestedCategory") == "plumbing" or data.get("category") == "plumbing":
                    self.test_service_request_id = data["id"]
                    self.log_result("service_requests", "Service Request Creation", True, 
                                  f"Request created with AI classification: {data.get('aiSuggestedCategory')} (confidence: {data.get('aiConfidence')})")
                    return True
                else:
                    self.log_result("service_requests", "Service Request Creation", False, 
                                  f"AI classification incorrect. Expected 'plumbing', got: {data.get('aiSuggestedCategory')}")
                    return False
            else:
                self.log_result("service_requests", "Service Request Creation", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("service_requests", "Service Request Creation", False, f"Exception: {str(e)}")
            return False

    def test_technician_matching(self):
        """Test technician matching for service request"""
        if not self.test_service_request_id:
            self.log_result("technician_matching", "Technician Matching", False, "No service request ID available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.get(f"{BACKEND_URL}/service-requests/{self.test_service_request_id}/matches", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    # Check if technicians have required fields
                    first_tech = data[0]
                    required_fields = ["id", "matchScore"]
                    missing_fields = [field for field in required_fields if field not in first_tech]
                    
                    if missing_fields:
                        self.log_result("technician_matching", "Technician Matching", False, f"Missing fields in technician: {missing_fields}")
                        return False
                    
                    # Check if technicians are ranked (sorted by matchScore)
                    scores = [tech.get("matchScore", 0) for tech in data]
                    is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
                    
                    if is_sorted:
                        self.test_technician_id = first_tech["id"]
                        self.log_result("technician_matching", "Technician Matching", True, 
                                      f"Found {len(data)} technicians, top match score: {first_tech.get('matchScore')}")
                        return True
                    else:
                        self.log_result("technician_matching", "Technician Matching", False, "Technicians not properly ranked by matchScore")
                        return False
                else:
                    self.log_result("technician_matching", "Technician Matching", False, "No technicians returned")
                    return False
            else:
                self.log_result("technician_matching", "Technician Matching", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("technician_matching", "Technician Matching", False, f"Exception: {str(e)}")
            return False

    def test_booking_creation(self):
        """Test booking creation with mock payment"""
        if not self.test_service_request_id or not self.test_technician_id:
            self.log_result("booking", "Booking Creation", False, "Missing service request ID or technician ID")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            payload = {
                "serviceRequestId": self.test_service_request_id,
                "technicianId": self.test_technician_id,
                "scheduledTime": "2025-01-25T10:00:00",
                "address": "Kadikoy, Istanbul",
                "estimatedPrice": "$150"
            }
            
            response = requests.post(f"{BACKEND_URL}/bookings", json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["id", "serviceRequestId", "technicianId", "status"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_result("booking", "Booking Creation", False, f"Missing fields: {missing_fields}")
                    return False
                
                self.test_booking_id = data["id"]
                
                # Verify service request status was updated
                sr_response = requests.get(f"{BACKEND_URL}/service-requests/{self.test_service_request_id}", headers=headers)
                if sr_response.status_code == 200:
                    sr_data = sr_response.json()
                    if sr_data.get("status") == "booked":
                        self.log_result("booking", "Booking Creation", True, 
                                      f"Booking created successfully, service request status updated to 'booked'")
                        return True
                    else:
                        self.log_result("booking", "Booking Creation", False, 
                                      f"Service request status not updated. Expected 'booked', got: {sr_data.get('status')}")
                        return False
                else:
                    self.log_result("booking", "Booking Creation", False, "Could not verify service request status update")
                    return False
            else:
                self.log_result("booking", "Booking Creation", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("booking", "Booking Creation", False, f"Exception: {str(e)}")
            return False

    def test_technician_jobs_listing(self):
        """Test technician jobs listing"""
        if not self.technician_token:
            self.log_result("technician_jobs", "Technician Jobs Listing", False, "No technician token available")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.technician_token}"}
            response = requests.get(f"{BACKEND_URL}/technician/jobs", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    # Check if jobs have required fields
                    if len(data) > 0:
                        first_job = data[0]
                        required_fields = ["id", "category", "descriptionText", "status"]
                        missing_fields = [field for field in required_fields if field not in first_job]
                        
                        if missing_fields:
                            self.log_result("technician_jobs", "Technician Jobs Listing", False, f"Missing fields in job: {missing_fields}")
                            return False
                    
                    self.log_result("technician_jobs", "Technician Jobs Listing", True, 
                                  f"Retrieved {len(data)} available jobs for technician")
                    return True
                else:
                    self.log_result("technician_jobs", "Technician Jobs Listing", False, "Response is not a list")
                    return False
            else:
                self.log_result("technician_jobs", "Technician Jobs Listing", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("technician_jobs", "Technician Jobs Listing", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all tests in priority order"""
        print("=" * 60)
        print("APPLIFIX BACKEND API TESTING SUITE")
        print("=" * 60)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test started at: {datetime.now()}")
        print("=" * 60)
        
        # HIGH PRIORITY TESTS
        print("\n🔥 HIGH PRIORITY TESTS")
        print("-" * 30)
        
        # 1. Authentication Flow
        print("\n1. AUTHENTICATION FLOW")
        self.test_auth_register_user()
        self.test_auth_register_technician()
        self.test_auth_login_user()
        self.test_auth_login_technician()
        
        # 2. Service Request Creation with AI
        print("\n2. SERVICE REQUEST CREATION WITH AI")
        self.test_service_request_creation_with_ai()
        
        # 3. Technician Matching
        print("\n3. TECHNICIAN MATCHING")
        self.test_technician_matching()
        
        # 4. Booking Creation
        print("\n4. BOOKING CREATION")
        self.test_booking_creation()
        
        # MEDIUM PRIORITY TESTS
        print("\n📋 MEDIUM PRIORITY TESTS")
        print("-" * 30)
        
        # 5. Technician Jobs Listing
        print("\n5. TECHNICIAN JOBS LISTING")
        self.test_technician_jobs_listing()
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_passed = 0
        total_failed = 0
        
        for category, results in self.results.items():
            passed = results["passed"]
            failed = results["failed"]
            total_passed += passed
            total_failed += failed
            
            status = "✅" if failed == 0 else "❌"
            print(f"{status} {category.upper().replace('_', ' ')}: {passed} passed, {failed} failed")
            
            # Print details for failed tests
            if failed > 0:
                for detail in results["details"]:
                    if "❌ FAIL" in detail:
                        print(f"   {detail}")
        
        print("-" * 60)
        overall_status = "✅ ALL TESTS PASSED" if total_failed == 0 else f"❌ {total_failed} TESTS FAILED"
        print(f"OVERALL: {total_passed} passed, {total_failed} failed - {overall_status}")
        print("=" * 60)
        
        return total_failed == 0

if __name__ == "__main__":
    tester = AppliFix_API_Tester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)