#!/usr/bin/env python3
"""
Debug script to test the API endpoint logic in isolation
"""
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app
from src.api.query_endpoint import QueryRequest, QueryContext

# Create a test client
client = TestClient(app)

print("Testing API endpoint with TestClient...")

# Test the query endpoint
response = client.post(
    "/api/query",
    json={
        "question": "What is Physical AI?",
        "context": {
            "search_scope": "full_book"
        }
    },
    headers={
        "Content-Type": "application/json"
    }
)

print(f"Response status: {response.status_code}")
print(f"Response JSON: {response.json()}")

if response.status_code != 200:
    print(f"Response text: {response.text}")