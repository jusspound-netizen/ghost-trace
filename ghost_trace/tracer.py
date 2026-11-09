import sqlite3
import json
import time
import functools

class GhostTracer:
    def __init__(self, db_path="ghost_trace.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS traces (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    tool_name TEXT,
                    arguments TEXT,
                    result TEXT,
                    error TEXT,
                    duration REAL
                )
            """)

    def trace(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            error = None
            result = None
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error = str(e)
                raise
            finally:
                duration = time.time() - start
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute(
                        "INSERT INTO traces (timestamp, tool_name, arguments, result, error, duration) VALUES (?, ?, ?, ?, ?, ?)",
                        (start, func.__name__, json.dumps(kwargs), str(result), error, duration)
                    )
        return wrapper

    def get_traces(self, limit=20):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute(
                "SELECT * FROM traces ORDER BY timestamp DESC LIMIT ?", (limit,)
            ).fetchall()
