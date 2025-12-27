#!/usr/bin/env python3
"""
Debug script to understand why the personalization route is not showing up
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_main_import():
    print("=== Debugging main.py import ===")

    # Step 1: Import each component individually
    print("\n1. Testing individual imports...")
    try:
        from fastapi import FastAPI
        print("+ FastAPI imported successfully")
    except Exception as e:
        print(f"- Error importing FastAPI: {e}")
        return

    try:
        from fastapi.middleware.cors import CORSMiddleware
        print("+ CORSMiddleware imported successfully")
    except Exception as e:
        print(f"- Error importing CORSMiddleware: {e}")
        return

    try:
        from src.api.personalize import router as personalize_router
        print("+ Personalize router imported successfully")
        print(f"  - Router path: {[route.path for route in personalize_router.routes]}")
    except Exception as e:
        print(f"- Error importing personalize router: {e}")
        import traceback
        traceback.print_exc()
        return

    try:
        from src.api.query_endpoint import router as query_router
        print("+ Query router imported successfully")
    except Exception as e:
        print(f"- Error importing query router: {e}")
        return

    try:
        from src.api.session_endpoint import router as session_router
        print("+ Session router imported successfully")
    except Exception as e:
        print(f"- Error importing session router: {e}")
        return

    # Step 2: Create app and add routers
    print("\n2. Creating app and adding routers...")
    try:
        app = FastAPI(
            title="AI Textbook Backend API",
            description="Backend API for AI-powered textbook features including chatbot and personalization",
            version="1.0.0"
        )
        print("+ App created successfully")
    except Exception as e:
        print(f"- Error creating app: {e}")
        return

    try:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        print("+ CORS middleware added successfully")
    except Exception as e:
        print(f"- Error adding CORS middleware: {e}")
        return

    try:
        app.include_router(
            personalize_router,
            prefix="/api",
            tags=["personalization"]
        )
        print("+ Personalize router added successfully")
    except Exception as e:
        print(f"- Error adding personalize router: {e}")
        import traceback
        traceback.print_exc()
        return

    try:
        app.include_router(
            query_router,
            prefix="/api",
            tags=["query"]
        )
        print("+ Query router added successfully")
    except Exception as e:
        print(f"- Error adding query router: {e}")
        return

    try:
        app.include_router(
            session_router,
            prefix="/api",
            tags=["session"]
        )
        print("+ Session router added successfully")
    except Exception as e:
        print(f"- Error adding session router: {e}")
        return

    # Step 3: Check routes
    print("\n3. Checking final routes...")
    routes = [route.path for route in app.routes]
    print(f"Final routes: {routes}")

    if "/api/personalize" in routes:
        print("+ /api/personalize route is present!")
    else:
        print("- /api/personalize route is MISSING!")
        print("Available routes:", routes)

    # Step 4: Test actual inclusion by creating a new app instance
    print("\n4. Testing by importing the actual main.py app...")
    try:
        from src.main import app as actual_app
        actual_routes = [route.path for route in actual_app.routes]
        print(f"Actual main.py routes: {actual_routes}")

        if "/api/personalize" in actual_routes:
            print("+ /api/personalize route is present in actual main.py!")
        else:
            print("- /api/personalize route is MISSING from actual main.py!")

    except Exception as e:
        print(f"- Error importing actual main app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_main_import()