from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "studyflow.db"

@dataclass(frozen=True)
class TaskRecord:
    id: int
    name: str
    subject: str
    deadline: str
    minutes: int
    difficulty: str
    notes: str
    completed: bool

class Storage:
    def __init__(self, path: Path = DB_PATH) -> None:
        self.path = path
        self._init_db()
        self._seed()

    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as c:
            c.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                deadline TEXT NOT NULL,
                minutes INTEGER NOT NULL,
                difficulty TEXT NOT NULL DEFAULT 'Medium',
                notes TEXT NOT NULL DEFAULT '',
                completed INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS focus_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                kind TEXT NOT NULL,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                planned_seconds INTEGER NOT NULL,
                actual_seconds INTEGER NOT NULL DEFAULT 0,
                completed INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY CHECK(id=1),
                name TEXT NOT NULL DEFAULT 'Student',
                age INTEGER NOT NULL DEFAULT 16,
                daily_goal INTEGER NOT NULL DEFAULT 120,
                subjects TEXT NOT NULL DEFAULT 'Mathematics,Physics,Programming,English',
                language TEXT NOT NULL DEFAULT 'en'
            );
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY CHECK(id=1),
                xp INTEGER NOT NULL DEFAULT 0,
                streak INTEGER NOT NULL DEFAULT 0,
                last_activity TEXT,
                total_goal_days INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS achievements (
                key TEXT PRIMARY KEY,
                unlocked_at TEXT
            );
            CREATE TABLE IF NOT EXISTS decorations (
                key TEXT PRIMARY KEY,
                unlocked INTEGER NOT NULL DEFAULT 0
            );
            """)
            c.execute("INSERT OR IGNORE INTO profile(id) VALUES(1)")
            c.execute("INSERT OR IGNORE INTO progress(id) VALUES(1)")
            columns = {r['name'] for r in c.execute('PRAGMA table_info(profile)').fetchall()}
            if 'language' not in columns:
                c.execute("ALTER TABLE profile ADD COLUMN language TEXT NOT NULL DEFAULT 'en'")
            for key in ("desk", "chair", "lamp", "books", "plant", "poster"):
                c.execute("INSERT OR IGNORE INTO decorations(key, unlocked) VALUES(?, ?)", (key, 1 if key in ("desk", "chair") else 0))

    def _seed(self):
        with self._connect() as c:
            if c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]:
                return
            today = date.today().isoformat()
            demos = [
                ("Algebra Practice", "Mathematics", today, 60, "Medium", "Focus on quadratic equations."),
                ("Physics Review", "Physics", (date.today() + timedelta(days=2)).isoformat(), 90, "Hard", "Review motion and forces."),
                ("Python OOP Lab", "Programming", (date.today() + timedelta(days=3)).isoformat(), 75, "Hard", "Classes, inheritance and composition."),
                ("English Essay", "English", (date.today() + timedelta(days=4)).isoformat(), 45, "Easy", "Write a first draft."),
            ]
            c.executemany("INSERT INTO tasks(name,subject,deadline,minutes,difficulty,notes) VALUES(?,?,?,?,?,?)", demos)

    def add_task(self, name, subject, deadline, minutes, difficulty, notes=""):
        with self._connect() as c:
            cur = c.execute("INSERT INTO tasks(name,subject,deadline,minutes,difficulty,notes) VALUES(?,?,?,?,?,?)", (name, subject, deadline, int(minutes), difficulty, notes))
            return int(cur.lastrowid)

    def list_tasks(self, pending_only=False):
        sql = "SELECT * FROM tasks"
        if pending_only:
            sql += " WHERE completed=0"
        sql += " ORDER BY completed, deadline, id"
        with self._connect() as c:
            rows = c.execute(sql).fetchall()
        return [TaskRecord(r["id"], r["name"], r["subject"], r["deadline"], r["minutes"], r["difficulty"], r["notes"], bool(r["completed"])) for r in rows]

    def get_task(self, task_id):
        with self._connect() as c:
            r = c.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not r:
            return None
        return TaskRecord(r["id"], r["name"], r["subject"], r["deadline"], r["minutes"], r["difficulty"], r["notes"], bool(r["completed"]))

    def set_completed(self, task_id, value=True):
        with self._connect() as c:
            c.execute("UPDATE tasks SET completed=? WHERE id=?", (int(value), task_id))

    def start_session(self, task_id, kind, planned_seconds):
        now = datetime.now().isoformat(timespec="seconds")
        with self._connect() as c:
            cur = c.execute("INSERT INTO focus_sessions(task_id,kind,started_at,planned_seconds) VALUES(?,?,?,?)", (task_id, kind, now, int(planned_seconds)))
            return int(cur.lastrowid)

    def finish_session(self, session_id, actual_seconds, completed):
        now = datetime.now().isoformat(timespec="seconds")
        with self._connect() as c:
            c.execute("UPDATE focus_sessions SET ended_at=?, actual_seconds=?, completed=? WHERE id=?", (now, max(0, int(actual_seconds)), int(completed), session_id))

    def get_profile(self):
        with self._connect() as c:
            r = c.execute("SELECT * FROM profile WHERE id=1").fetchone()
        return dict(r)

    def update_profile(self, name, age, daily_goal, subjects, language=None):
        with self._connect() as c:
            if language is None:
                c.execute(
                    "UPDATE profile SET name=?, age=?, daily_goal=?, subjects=? WHERE id=1",
                    (name, int(age), int(daily_goal), subjects),
                )
            else:
                c.execute(
                    "UPDATE profile SET name=?, age=?, daily_goal=?, subjects=?, language=? WHERE id=1",
                    (name, int(age), int(daily_goal), subjects, language),
                )

    def get_progress(self):
        with self._connect() as c:
            return dict(c.execute("SELECT * FROM progress WHERE id=1").fetchone())

    def add_xp(self, amount):
        with self._connect() as c:
            c.execute("UPDATE progress SET xp=xp+? WHERE id=1", (int(amount),))

    def register_activity(self, day=None):
        d = day or date.today()
        with self._connect() as c:
            row = c.execute("SELECT streak,last_activity FROM progress WHERE id=1").fetchone()
            streak = int(row["streak"])
            last = row["last_activity"]
            if last == d.isoformat():
                return streak
            if last:
                gap = (d - date.fromisoformat(last)).days
                streak = streak + 1 if gap == 1 else 1
            else:
                streak = 1
            c.execute("UPDATE progress SET streak=?, last_activity=? WHERE id=1", (streak, d.isoformat()))
            return streak

    def unlock_achievement(self, key):
        with self._connect() as c:
            c.execute("INSERT OR IGNORE INTO achievements(key,unlocked_at) VALUES(?,?)", (key, datetime.now().isoformat(timespec="seconds")))

    def achievements(self):
        with self._connect() as c:
            return {r["key"] for r in c.execute("SELECT key FROM achievements").fetchall()}

    def unlock_decoration(self, key):
        with self._connect() as c:
            c.execute("UPDATE decorations SET unlocked=1 WHERE key=?", (key,))

    def decorations(self):
        with self._connect() as c:
            return {r["key"]: bool(r["unlocked"]) for r in c.execute("SELECT key,unlocked FROM decorations").fetchall()}

    def total_study_seconds(self, start=None, end=None):
        clauses=["kind='study'"]
        args=[]
        if start:
            clauses.append("date(started_at)>=date(?)"); args.append(start.isoformat())
        if end:
            clauses.append("date(started_at)<=date(?)"); args.append(end.isoformat())
        with self._connect() as c:
            v=c.execute(f"SELECT COALESCE(SUM(actual_seconds),0) FROM focus_sessions WHERE {' AND '.join(clauses)}", args).fetchone()[0]
        return int(v or 0)

    def subject_minutes(self, start, end):
        with self._connect() as c:
            rows=c.execute("""
                SELECT COALESCE(t.subject,'Other') subject, COALESCE(SUM(f.actual_seconds),0) secs
                FROM focus_sessions f LEFT JOIN tasks t ON t.id=f.task_id
                WHERE f.kind='study' AND date(f.started_at) BETWEEN date(?) AND date(?)
                GROUP BY t.subject ORDER BY secs DESC
            """, (start.isoformat(), end.isoformat())).fetchall()
        return [(r["subject"], int(r["secs"]//60)) for r in rows]

    def completed_count(self):
        with self._connect() as c:
            return int(c.execute("SELECT COUNT(*) FROM tasks WHERE completed=1").fetchone()[0])
