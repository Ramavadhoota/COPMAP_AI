import os
import sqlite3
from datetime import datetime, timezone

DB_PATH = os.path.join("copmap-poc", "data", "copmap.db")

def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    con = sqlite3.connect(DB_PATH)
    try:
        con.execute("PRAGMA foreign_keys = ON;")

        # --- schema (minimal PoC) ---
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS officers (
              id TEXT PRIMARY KEY,
              name TEXT NOT NULL,
              role TEXT NOT NULL DEFAULT 'field',
              last_lat REAL,
              last_lon REAL,
              last_seen_at TEXT
            );

            CREATE TABLE IF NOT EXISTS patrols (
              id TEXT PRIMARY KEY,
              officer_id TEXT NOT NULL,
              start_time TEXT NOT NULL,
              end_time TEXT,
              start_lat REAL,
              start_lon REAL,
              location_text TEXT,
              summary TEXT,
              risk_score REAL,
              FOREIGN KEY (officer_id) REFERENCES officers(id)
            );

            CREATE TABLE IF NOT EXISTS alerts (
              id TEXT PRIMARY KEY,
              type TEXT NOT NULL,
              priority TEXT NOT NULL,
              lat REAL NOT NULL,
              lon REAL NOT NULL,
              confidence REAL NOT NULL,
              status TEXT NOT NULL DEFAULT 'open',
              assigned_officer_id TEXT,
              metadata_json TEXT,
              created_at TEXT NOT NULL,
              resolved_at TEXT,
              FOREIGN KEY (assigned_officer_id) REFERENCES officers(id)
            );

            CREATE TABLE IF NOT EXISTS incidents (
              id TEXT PRIMARY KEY,
              patrol_id TEXT,
              alert_id TEXT,
              type TEXT NOT NULL,
              description TEXT NOT NULL,
              lat REAL,
              lon REAL,
              ts TEXT NOT NULL,
              evidence_urls_json TEXT,
              FOREIGN KEY (patrol_id) REFERENCES patrols(id),
              FOREIGN KEY (alert_id) REFERENCES alerts(id)
            );
            """
        )

        # --- seed data ---
        con.execute(
            "INSERT OR REPLACE INTO officers (id,name,role,last_lat,last_lon,last_seen_at) VALUES (?,?,?,?,?,?)",
            ("officer_1", "Officer A", "field", 12.9716, 77.5946, iso_now()),
        )
        con.execute(
            "INSERT OR REPLACE INTO officers (id,name,role,last_lat,last_lon,last_seen_at) VALUES (?,?,?,?,?,?)",
            ("officer_2", "Officer B", "field", 12.9750, 77.6000, iso_now()),
        )

        con.execute(
            "INSERT OR REPLACE INTO patrols (id,officer_id,start_time,start_lat,start_lon,location_text) VALUES (?,?,?,?,?,?)",
            ("patrol_demo_1", "officer_1", iso_now(), 12.9716, 77.5946, "Sector 15"),
        )

        con.execute(
            """INSERT OR REPLACE INTO alerts
               (id,type,priority,lat,lon,confidence,status,assigned_officer_id,metadata_json,created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                "alert_demo_1",
                "crowd_density",
                "P2",
                12.9716,
                77.5946,
                0.89,
                "open",
                "officer_1",
                '{"person_count":210,"area_sqm":60,"density":3.5,"source":"mock_camera_1"}',
                iso_now(),
            ),
        )

        con.execute(
            """INSERT OR REPLACE INTO incidents
               (id,patrol_id,alert_id,type,description,lat,lon,ts,evidence_urls_json)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                "incident_demo_1",
                "patrol_demo_1",
                "alert_demo_1",
                "crowd_check",
                "Crowd observed near junction; officer verified and monitored.",
                12.9716,
                77.5946,
                iso_now(),
                '["local://photo1.jpg"]',
            ),
        )

        con.commit()
        print(" created:", os.path.abspath(DB_PATH))
    finally:
        con.close()

if __name__ == "__main__":
    main()
