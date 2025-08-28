"""
API Endpoint Test Script for AI Dungeon Master Backend
Checks all endpoints for health and basic responses
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

# Utility function to print results
def print_result(endpoint, response):
    print(f"\n[TEST] {endpoint}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)

# 1. Health check
resp = requests.get(f"{BASE_URL}/health")
print_result("GET /health", resp)

# 2. Start game
resp = requests.post(f"{BASE_URL}/start-game", json={"player_name": "TestHero"})
print_result("POST /start-game", resp)
assert resp.status_code == 200 and resp.json().get("success"), "Start game failed"
session_id = resp.json().get("session_id")

# 3. Make choice (first choice)
resp = requests.post(f"{BASE_URL}/make-choice", json={"session_id": session_id, "choice_index": 0})
print_result("POST /make-choice", resp)
assert resp.status_code == 200 and resp.json().get("success"), "Make choice failed"

# 4. Get stats
resp = requests.post(f"{BASE_URL}/get-stats", json={"session_id": session_id})
print_result("POST /get-stats", resp)
assert resp.status_code == 200 and resp.json().get("success"), "Get stats failed"

# 5. Save game
resp = requests.post(f"{BASE_URL}/save-game", json={"session_id": session_id, "save_name": "apitest_save"})
print_result("POST /save-game", resp)
assert resp.status_code == 200 and resp.json().get("success"), "Save game failed"

# 6. Get history
resp = requests.post(f"{BASE_URL}/get-history", json={"session_id": session_id, "limit": 5})
print_result("POST /get-history", resp)
assert resp.status_code == 200 and resp.json().get("success"), "Get history failed"

# 7. End session
resp = requests.post(f"{BASE_URL}/end-session", json={"session_id": session_id})
print_result("POST /end-session", resp)
assert resp.status_code == 200 and resp.json().get("success"), "End session failed"

# 8. Get active sessions
resp = requests.get(f"{BASE_URL}/sessions")
print_result("GET /sessions", resp)
assert resp.status_code == 200 and resp.json().get("success"), "Get sessions failed"

print("\n✅ All API endpoint tests completed!")
