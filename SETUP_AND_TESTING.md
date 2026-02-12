# COPMAP AI - Setup & Testing Guide

## Overview
COPMAP AI is a Police Monitoring and Community Accountability Platform with RAG-based video search capabilities. This document covers setup, testing, and usage.

## Quick Start

### Prerequisites
- Python 3.12+
- Ubuntu 24.04 LTS (or compatible Linux)
- 4GB+ RAM
- pip package manager

### Installation & Setup

1. **Clone and navigate to the project:**
```bash
cd /workspaces/COPMAP_AI/copmap-poc
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
bash /workspaces/COPMAP_AI/verify_install.sh
```

4. **Start the server:**
```bash
python3 -m uvicorn app.main:create_app --host 0.0.0.0 --port 8000 --factory
```

### Running Tests

**Test video processing with sample videos:**
```bash
python3 /workspaces/COPMAP_AI/test_video_processing.py
```

This will:
- Ingest 4 sample videos into the RAG system
- Execute 6 semantic search queries
- Display similarity scores and results
- Verify API endpoints are working

## Architecture

### Key Components

1. **FastAPI Application** (`app/main.py`)
   - RESTful API endpoints
   - WebSocket support for live officer updates
   - CORS middleware enabled

2. **Routers** (`app/routers/`)
   - `health.py` - Health check endpoint
   - `documents.py` - Video/document ingestion
   - `rag.py` - Semantic search queries
   - `alerts.py` - Alert management
   - `patrols.py` - Patrol tracking

3. **Services** (`app/services/`)
   - `rag_service.py` - Vector embeddings and search
   - `llm_service.py` - LLM integration
   - `alert_service.py` - Alert handling
   - `patrol_service.py` - Patrol management

4. **Database**
   - SQLAlchemy ORM for relational data
   - ChromaDB for vector embeddings
   - SQLite for persistence

## API Endpoints

### Health & Status
```
GET /health
```
Check if the server is running.

**Response:**
```json
{"status": "ok"}
```

### Video Ingestion
```
POST /api/v1/documents/ingest
```
Ingest video metadata into the RAG system.

**Request:**
```json
{
  "doc_id": "video_001",
  "doc_type": "video",
  "content": "Detailed description of video content...",
  "metadata": {
    "video_name": "Downtown Patrol - Traffic Stop",
    "location": "Main St & 5th Ave",
    "officer_id": "OFF_001",
    "timestamp": "2026-02-12 14:30:00"
  }
}
```

**Response:**
```json
{"status": "ingested", "doc_id": "video_001"}
```

### Semantic Search
```
POST /api/v1/rag/query
```
Search for videos using natural language queries.

**Request:**
```json
{
  "query": "traffic stop and speeding",
  "k": 5,
  "filters": {}
}
```

**Response:**
```json
{
  "query": "traffic stop and speeding",
  "results": [
    {
      "distance": 0.394,
      "content": "...",
      "metadata": {
        "video_name": "Downtown Patrol - Traffic Stop",
        "location": "Main St & 5th Ave",
        "officer_id": "OFF_001",
        "timestamp": "2026-02-12 14:30:00"
      }
    }
  ]
}
```

## Dependencies

### ML & Embeddings
- **torch**: 2.10.0+cpu (PyTorch CPU version)
- **numpy**: 1.26.4 (Numerical computing)
- **transformers**: 4.57.6 (Pre-trained models)
- **sentence-transformers**: 2.7.0 (Sentence embeddings)
- **chromadb**: 1.5.0 (Vector database)

### Web Framework
- **fastapi**: ≥0.110
- **uvicorn**: ≥0.25

### Database & ORM
- **SQLAlchemy**: ≥2.0
- **pydantic**: ≥2.5

## Sample Videos

Located in `sample_videos/` directory:

1. **video_001_metadata.json**
   - Downtown Patrol - Traffic Stop
   - Location: Main St & 5th Ave
   - Officer: OFF_001

2. **video_002_metadata.json**
   - Park Patrol - Disturbance Call
   - Location: Central Park
   - Officer: OFF_002

3. **video_003_metadata.json**
   - Highway Patrol - Vehicle Inspection
   - Location: Highway 101 South
   - Officer: OFF_003

4. **video_004_metadata.json**
   - Downtown Patrol - Suspicious Activity
   - Location: Downtown Industrial Area
   - Officer: OFF_001

## Testing

### Running the Test Suite
```bash
python3 test_video_processing.py
```

### Test Output
The test script will:
1. Check server health
2. Ingest 4 sample videos
3. Wait for indexing (2 seconds)
4. Execute 6 semantic search queries
5. Display results with similarity scores

### Example Test Queries
- "traffic stop and speeding" → Distance: 0.394
- "suspicious activity downtown" → Distance: 0.502
- "vehicle safety inspection" → Distance: 0.969
- "park disturbance" → Distance: 0.609
- "Officer OFF_001 activities" → Multiple results
- "highway patrol" → Distance: 0.964

## Configuration

### Environment Variables
See `copmap-poc/.env.example` for configuration options.

Key variables:
```
DATABASE_URL=sqlite:///./test.db
DATA_DIR=./data
CORS_ORIGINS=*
APP_NAME=COPMAP
```

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'torch'

**Solution:**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Issue: ChromaDB version conflicts

**Solution:**
```bash
pip uninstall chromadb sentence-transformers transformers torch numpy
pip install -r requirements.txt
```

### Issue: Port 8000 already in use

**Solution:**
```bash
lsof -i :8000
kill -9 <PID>
```

## Development

### Adding New Videos

1. Create a new JSON file in `sample_videos/`:
```json
{
  "video_id": "video_005",
  "video_name": "Your Video Name",
  "description": "Detailed description...",
  "timestamp": "2026-02-12 18:00:00",
  "location": "Location Name",
  "officer_id": "OFF_XXX",
  "video_type": "body_cam",
  "duration_seconds": 600,
  "file_size_mb": 400,
  "status": "processed",
  "tags": ["tag1", "tag2"]
}
```

2. Ingest using the API:
```bash
curl -X POST http://localhost:8000/api/v1/documents/ingest \
  -H "Content-Type: application/json" \
  -d '{...}'
```

### Running in Development Mode

```bash
cd copmap-poc
python3 -m uvicorn app.main:create_app --reload --host 0.0.0.0 --port 8000 --factory
```

## Documentation

- **API Docs (Swagger UI)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Files Structure

```
COPMAP_AI/
├── copmap-poc/
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── config.py                  # Configuration
│   │   ├── schemas.py                 # Pydantic models
│   │   ├── routers/                   # API routes
│   │   └── services/                  # Business logic
│   ├── requirements.txt                # Python dependencies
│   ├── docker-compose.yml             # Docker config
│   └── Dockerfile                     # Container image
├── sample_videos/                      # Test video metadata
├── test_video_processing.py           # Test suite
├── verify_install.sh                  # Dependency checker
└── README.md                          # This file
```

## Support & Contribution

For issues or improvements:
1. Check existing issues in GitHub
2. Create a new issue with details
3. Submit a pull request with changes

## License

Refer to the project LICENSE file.

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
