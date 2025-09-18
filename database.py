"""Database utilities for the TORIM application."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from werkzeug.security import check_password_hash, generate_password_hash


class UserDatabase:
    """Lightweight SQLite based storage for application users."""

    def __init__(self, db_path: str = "torim.db") -> None:
        self.db_path = Path(db_path)
        # Ensure parent directory exists when a custom path is provided
        if self.db_path.parent != Path("."):
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _get_connection(self) -> sqlite3.Connection:
        """Create a new database connection with safe defaults."""
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        """Create required tables and seed the default user."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT,
                    avatar TEXT,
                    reliability INTEGER DEFAULT 0,
                    referral_code TEXT,
                    referred_friends INTEGER DEFAULT 0,
                    is_business_owner INTEGER DEFAULT 0,
                    business_id INTEGER,
                    password_hash TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        self._ensure_seed_user()

    def _ensure_seed_user(self) -> None:
        """Ensure the demo user from the legacy in-memory dataset exists."""
        if self.get_user_by_email("yossi@example.com"):
            return

        self.create_user(
            name="יוסי לוי",
            email="yossi@example.com",
            phone="050-1234567",
            avatar="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150",
            reliability=95,
            referral_code="YOSSI2025",
            referred_friends=3,
            is_business_owner=True,
            business_id=1,
            password="ChangeMe!2025",
        )

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert a SQLite row into a serialisable dictionary."""
        return {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "phone": row["phone"],
            "avatar": row["avatar"],
            "reliability": row["reliability"],
            "referral_code": row["referral_code"],
            "referred_friends": row["referred_friends"],
            "is_business_owner": bool(row["is_business_owner"]),
            "business_id": row["business_id"],
            "created_at": row["created_at"],
        }

    def create_user(
        self,
        *,
        name: str,
        email: str,
        phone: Optional[str] = None,
        avatar: Optional[str] = None,
        reliability: int = 0,
        referral_code: Optional[str] = None,
        referred_friends: int = 0,
        is_business_owner: bool = False,
        business_id: Optional[int] = None,
        password: str,
    ) -> Dict[str, Any]:
        """Create a new user with a securely hashed password."""
        password_hash = generate_password_hash(password)
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO users (
                    name, email, phone, avatar, reliability, referral_code,
                    referred_friends, is_business_owner, business_id, password_hash
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    email,
                    phone,
                    avatar,
                    reliability,
                    referral_code,
                    referred_friends,
                    int(is_business_owner),
                    business_id,
                    password_hash,
                ),
            )
            user_id = cursor.lastrowid
        return self.get_user_by_id(user_id)

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if row is None:
            return None
        return self._row_to_dict(row)

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if row is None:
            return None
        return self._row_to_dict(row)

    def list_users(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM users ORDER BY created_at DESC"
            ).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def verify_user_credentials(self, email: str, password: str) -> bool:
        """Safely verify a user's password without exposing the hash."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT password_hash FROM users WHERE email = ?", (email,)
            ).fetchone()
        if row is None:
            return False
        return check_password_hash(row["password_hash"], password)

    def update_password(self, user_id: int, new_password: str) -> bool:
        """Update a user's password using hashing. Returns True when updated."""
        password_hash = generate_password_hash(new_password)
        with self._get_connection() as conn:
            cursor = conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (password_hash, user_id),
            )
            return cursor.rowcount == 1

