from pathlib import Path

paths = [
    "copmap-poc/README.md",
    "copmap-poc/.env.example",
    "copmap-poc/requirements.txt",
    "copmap-poc/docker-compose.yml",

    "copmap-poc/data/copmap.db",
    "copmap-poc/data/samples/sop.md",
    "copmap-poc/data/samples/patrol_log.json",
    "copmap-poc/data/samples/alert.json",

    "copmap-poc/app/main.py",
    "copmap-poc/app/config.py",
    "copmap-poc/app/db.py",
    "copmap-poc/app/models.py",
    "copmap-poc/app/schemas.py",
    "copmap-poc/app/ws.py",

    "copmap-poc/app/services/alert_service.py",
    "copmap-poc/app/services/rag_service.py",
    "copmap-poc/app/services/llm_service.py",
    "copmap-poc/app/services/patrol_service.py",

    "copmap-poc/app/routers/health.py",
    "copmap-poc/app/routers/alerts.py",
    "copmap-poc/app/routers/patrols.py",
    "copmap-poc/app/routers/rag.py",
    "copmap-poc/app/routers/documents.py",

    "copmap-poc/scripts/seed_demo.py",

    "copmap-poc/tests/test_alerts.py",
    "copmap-poc/tests/test_rag.py",
]

for p in paths:
    path = Path(p)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

print("✅ copmap-poc structure created successfully")
