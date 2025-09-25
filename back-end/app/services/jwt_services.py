from flask import current_app

from app.utils import now_utc

from datetime import timedelta

import jwt


class JWTService:
    @staticmethod
    def create_access_token(subject: str, role: str = "user", expire_minutes: int = 15):
        now = now_utc()
        payload = {
            "sub": subject,
            "type": "access",
            "role": role,
            "iat": now,
            "exp": now + timedelta(minutes=expire_minutes)
        }
        return jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def create_refresh_token(subject: str, expire_days: int = 7):
        now = now_utc()
        payload = {
            "sub": subject,
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=expire_days)
        }
        return jwt.encode(payload, current_app.config["JWT_REFRESH_SECRET_KEY"], algorithm="HS256")
