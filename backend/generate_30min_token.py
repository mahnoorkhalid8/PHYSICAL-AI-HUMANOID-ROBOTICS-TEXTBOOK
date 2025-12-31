#!/usr/bin/env python3
"""
Generate a JWT token that expires in 30 minutes for testing purposes
"""
import jwt
import json
from datetime import datetime, timedelta

# Get the private key from the JWKS server
private_key_pem = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDG+MWXMRq3uxGh
pH5xQtSPvUwVcCC45xKqs8DIMsPEb6euRo+JdomnvNC3IuZPH7MBTFm7KPXjpgd+
IYOvBu57Kyh+0XLwZet8wLgoiNnxh5x0z60qm+eCt0HL4JzQGXduSo90ngCY06FP
X5vBXB+MQUTpRt1v8uyafrbK4WmCVp7a7IaFcKGM471Ue89lOBpkP1eph3KlAmGV
WA10cPV7om0h5ZT8sGCSh2pnTXiOarEuQN9ugH1Xd1fCfTOXwPh3S3KCGSH35dWd
rfyQ+GGkqPHojoG16CePBuUAAGQluGjdW+F3v7V1myyzybynLKmVibiJn6dwfmHC
jodEJZkFAgMBAAECggEAQkAkHocBo+qcYMuSNGkxuJippDu9EYQTMZZ/mslYaOha
l0s0UOuQwzK59jifIfpmkoiXGhv137JxLTzAiX9P2eARcESSNlxhUB0lVI3Yr7Td
UgGyYY0exWX6eQWVgS7xlt4prQVNIpXY0MJ/bJ8dfAhhhyEK61MiGAEYIS50AKr7
Qhy04xLpSFi+OQlcZmX7dtOck5uSrVmUBPLtXMkl6PuIwLSoYK6J0oSlOTgFlvjB
7Pr6k5LNB+J+dEp4zAQ3MExq7Vvs5YA7KDHlXqRJNTbNP8CSNkBx4Jnj/5FfzwTN
k9pup7ertKAE2LC8QU/jX56rL3vKnFO1SsQPhCAGkwKBgQDxLJYx4eCLhaajzurR
f0FJAMpWK0uFnXkJ/IUeTFVlq0neyTlt4XlNBb+zaC/fjz1bM3nTQEtZNsowRypM
jtZH3Uvi8NHb8AayPsebh52V4yFkzMgyTPhOp+xg3zkB1DxBk4IWZdZIWD22O7Zv
1eUJgtKBUVTLv91SUaLqwkMStwKBgQDTNAlHHvIm2SmnYdlDxjPM1UIQDiSrrgQS
xITMZkLjteLVQsJNCsq9x6fBWGnNWtHjvyiux3bQKCqsBXy2cuG/fR0sqVLuhSa+
5Y9Uh7+hXrDqxcXUYht4MvTl0rB0yPawOSCX0aYAA4GRI2VnaZC6bw3hAkHV4yc3
DY/NhQRGIwKBgFksSzyWcBgmir72uwxLKTB9AlNqHrqAx0hR/kZ9ovW8p8ugS4O9
YsR/46nKVCktJVqbZegeVb3e7FN9fL5h8gkQYga/VFkmHtO5MsTnF/VbzfUfYsZ2
fzlWDaij4Mg0WTNF/0uYy+pj9i1zVrlzNQSXQo5eLCRKBONzG/IBchtxAoGAYFaO
HNjqz/mi3Gzvs9CG9FoahkRNSdpYlU763FmRDVl8HJcVFhtkG2klBjaUHE3fC6m4
nvDxK0YHIOxn1LlWbAhf9G1QHOizocQIuyAosy0EOjL4aEZQDWYA+4w9XSgGDqAg
U+AXfk4bHd8tdBxdHg1mIUrsSOoSizQucirIpk0CgYBl1Blg8Y+XbVOuauvOrZ5v
dLgN+MyQdig6vBkkPFa19rYMz/3K8+XpXTjHuQuzpMCVXw/WnIrWHL4o9PvVXdNr
r0NPa2TW7Ex322Fx+sF6fPrJhTMCk2CG/KgkgVaSmcO52nVFkH+btTf1XQJQ6QLF
PiZ+zJQwumL2uxUwV6d2Zg==
-----END PRIVATE KEY-----"""

# Define the payload that matches what the system expects
payload = {
    "sub": "test-user-123",  # User ID (matches the user_id in the request)
    "email": "test@example.com",
    "name": "Test User",
    "user_metadata": {
        "software_background": "Intermediate Python developer with robotics experience",
        "hardware_background": "Basic understanding of electronic circuits"
    },
    "iat": int(datetime.utcnow().timestamp()),  # Issued at
    "exp": int((datetime.utcnow() + timedelta(minutes=30)).timestamp()),  # Expires in 30 minutes
    "nbf": int(datetime.utcnow().timestamp()),  # Not before
    "iss": "test-auth-server",  # Issuer
    "aud": "test-app",  # Audience
    "kid": "test-key-id"  # Key ID (must match JWKS)
}

# Generate the RS256 token using the private key
token = jwt.encode(payload, private_key_pem, algorithm="RS256", headers={"kid": "test-key-id"})

print("Generated 30-minute JWT Token (RS256):")
print(token)
print("\nPayload:")
print(json.dumps(payload, indent=2))

# Also create a sample request body for the API
request_body = {
    "chapter_content": "This chapter covers the fundamentals of humanoid robotics, including kinematics, dynamics, control systems, and gait planning. We'll explore how robots can mimic human movement patterns and maintain balance while walking. The chapter includes mathematical models for legged locomotion, sensor fusion techniques, and real-time control algorithms.",
    "chapter_title": "Introduction to Humanoid Robotics",
    "user_id": "test-user-123",
    "user_background": {
        "software": "Intermediate Python developer with robotics experience",
        "hardware": "Basic understanding of electronic circuits"
    }
}

print("\nSample request body for personalization API:")
print(json.dumps(request_body, indent=2))

print("\nComplete curl command:")
print(f'curl -X POST http://localhost:8000/api/personalize -H "Content-Type: application/json" -H "Authorization: Bearer {token}" -d \'{json.dumps(request_body)}\'')