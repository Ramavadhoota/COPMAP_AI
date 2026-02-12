#!/usr/bin/env python3
"""
Test script for COPMAP video processing using the RAG API
This script:
1. Creates sample video metadata
2. Ingests it into the RAG system
3. Queries for relevant information
"""

import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Test the health endpoint"""
    print("=" * 60)
    print("Testing Health Endpoint")
    print("=" * 60)
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def ingest_video_metadata(video_id, video_name, description, timestamp, location, officer_id):
    """Ingest video metadata into the RAG system"""
    print("=" * 60)
    print(f"Ingesting Video: {video_name}")
    print("=" * 60)
    
    # Create comprehensive video content for RAG embedding
    video_content = f"""
    Video ID: {video_id}
    Title: {video_name}
    Description: {description}
    Recording Time: {timestamp}
    Location: {location}
    Officer ID: {officer_id}
    
    Content Summary: {description}
    """
    
    payload = {
        "doc_id": video_id,
        "doc_type": "video",
        "content": video_content,
        "metadata": {
            "video_name": video_name,
            "location": location,
            "officer_id": officer_id,
            "timestamp": timestamp,
            "video_type": "body_cam"
        }
    }
    
    response = requests.post(
        f"{API_BASE_URL}/documents/ingest",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    return response.status_code == 200

def query_videos(query_text, k=5):
    """Query the RAG system for relevant videos"""
    print("=" * 60)
    print(f"Querying: {query_text}")
    print("=" * 60)
    
    payload = {
        "query": query_text,
        "k": k,
        "filters": {}
    }
    
    response = requests.post(
        f"{API_BASE_URL}/rag/query",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Query: {result.get('query')}")
    print(f"Results Found: {len(result.get('results', []))}")
    
    if result.get('results'):
        for i, result_item in enumerate(result['results'], 1):
            print(f"\n  Result {i}:")
            print(f"    Distance: {result_item.get('distance', 'N/A')}")
            print(f"    Content Preview: {result_item.get('content', '')[:100]}...")
            if result_item.get('metadata'):
                print(f"    Metadata: {result_item.get('metadata')}")
    print()
    return response.status_code == 200

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("COPMAP VIDEO PROCESSING TEST")
    print("=" * 60 + "\n")
    
    # Test health
    if not test_health():
        print("❌ Server is not responding!")
        return
    
    # Sample video metadata
    test_videos = [
        {
            "id": "video_001",
            "name": "Downtown Patrol - Traffic Stop",
            "description": "Traffic stop at intersection of Main and 5th Street. Vehicle speeding detected. Driver cooperative.",
            "timestamp": "2026-02-12 14:30:00",
            "location": "Main St & 5th Ave",
            "officer_id": "OFF_001"
        },
        {
            "id": "video_002",
            "name": "Park Patrol - Disturbance Call",
            "description": "Response to disturbance call at Central Park. Two individuals arguing over parking. Situation resolved peacefully.",
            "timestamp": "2026-02-12 15:45:00",
            "location": "Central Park",
            "officer_id": "OFF_002"
        },
        {
            "id": "video_003",
            "name": "Highway Patrol - Vehicle Inspection",
            "description": "Routine vehicle safety inspection on Highway 101. Faulty brake lights detected. Owner notified and ticket issued.",
            "timestamp": "2026-02-12 16:20:00",
            "location": "Highway 101 South",
            "officer_id": "OFF_003"
        },
        {
            "id": "video_004",
            "name": "Downtown Patrol - Suspicious Activity",
            "description": "Investigation of suspicious activity behind downtown buildings. Found discarded bag. Area secured pending investigation team arrival.",
            "timestamp": "2026-02-12 17:00:00",
            "location": "Downtown Industrial Area",
            "officer_id": "OFF_001"
        }
    ]
    
    # Ingest videos
    print("\n📹 PHASE 1: INGESTING VIDEO METADATA")
    print("=" * 60 + "\n")
    
    for video in test_videos:
        success = ingest_video_metadata(
            video_id=video["id"],
            video_name=video["name"],
            description=video["description"],
            timestamp=video["timestamp"],
            location=video["location"],
            officer_id=video["officer_id"]
        )
        if success:
            print(f"✓ {video['name']} ingested successfully\n")
        else:
            print(f"✗ Failed to ingest {video['name']}\n")
    
    # Wait a moment for indexing
    print("\n⏳ Waiting for indexing...\n")
    import time
    time.sleep(2)
    
    # Test queries
    print("\n🔍 PHASE 2: QUERYING VIDEOS")
    print("=" * 60 + "\n")
    
    test_queries = [
        "traffic stop and speeding",
        "suspicious activity downtown",
        "vehicle safety inspection",
        "park disturbance",
        "Officer OFF_001 activities",
        "highway patrol"
    ]
    
    for query in test_queries:
        query_videos(query, k=3)
    
    print("\n" + "=" * 60)
    print("✓ VIDEO PROCESSING TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
