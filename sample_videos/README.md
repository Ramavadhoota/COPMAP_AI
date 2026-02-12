# Sample Videos - COPMAP AI

This directory contains sample video metadata files for testing the COPMAP AI video processing and RAG system.

## Files

### Video Metadata Files
- `video_001_metadata.json` - Downtown Patrol - Traffic Stop
- `video_002_metadata.json` - Park Patrol - Disturbance Call
- `video_003_metadata.json` - Highway Patrol - Vehicle Inspection
- `video_004_metadata.json` - Downtown Patrol - Suspicious Activity

## Metadata Structure

Each video metadata file contains:
```json
{
  "video_id": "unique_identifier",
  "video_name": "descriptive_name",
  "description": "detailed_description",
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "location": "geographic_location",
  "officer_id": "officer_identifier",
  "video_type": "body_cam",
  "duration_seconds": 420,
  "file_size_mb": 340,
  "status": "processed",
  "tags": ["tag1", "tag2"]
}
```

## Usage

### Loading Sample Videos
```python
import json

# Load a sample video
with open('sample_videos/video_001_metadata.json', 'r') as f:
    video_data = json.load(f)
```

### Ingesting into RAG System
```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "video_001",
    "doc_type": "video",
    "content": "Video metadata here...",
    "metadata": {
      "video_name": "Downtown Patrol - Traffic Stop",
      "location": "Main St & 5th Ave",
      "officer_id": "OFF_001"
    }
  }'
```

### Testing with the Test Script
```bash
python3 test_video_processing.py
```

## Adding New Videos

1. Create a new JSON file: `video_XXX_metadata.json`
2. Follow the metadata structure above
3. Update the test script to include new videos
4. Ingest into the system using the API

## Video Types

- `body_cam` - Body-worn camera footage
- `dash_cam` - Dashboard camera from patrol vehicle
- `cctv` - Surveillance camera footage
- `intersection_camera` - Traffic intersection footage

## Tags

Common tags for categorization:
- `traffic` - Traffic-related incidents
- `disturbance` - Disturbance/noise complaints
- `safety` - Safety violations
- `investigation` - Criminal investigation
- `patrol` - Routine patrol
- `downtown` - Downtown area
- `highway` - Highway area
- `park` - Park area

## Notes

- All timestamps are in UTC format (YYYY-MM-DD HH:MM:SS)
- Location should be specific and queryable
- Officer IDs should match those in the patrol management system
- Tags help with semantic search and categorization
