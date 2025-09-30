from flask_jwt_extended import create_access_token, create_refresh_token


class JWTService:
    @staticmethod
    def create_access_token(subject: str, role: str = "user"):
        return create_access_token(
            identity=subject,
            additional_claims={
                "type": "access",
                "role": role,
                "permissions": ["create", "read", "update", "delete"],
                "is_verified": True
            }
        )

    @staticmethod
    def create_refresh_token(subject: str, role: str = "user"):
        return create_refresh_token(
            identity=subject,
            additional_claims={
                "type": "refresh",
                "role": role,
                "is_active": True
            }
        )
