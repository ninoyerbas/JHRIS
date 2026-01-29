"""
Authentication service layer.
"""
from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.auth import utils, schemas
from app.users import service as user_service
from app.users.models import User
from app.config import settings


class AuthService:
    """Service class for authentication operations."""
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            db: Database session
            email: User email
            password: User password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        return user_service.UserService.authenticate(db, email, password)
    
    @staticmethod
    def create_tokens(user_id: int) -> schemas.Token:
        """
        Create access and refresh tokens for user.
        
        Args:
            user_id: User ID
            
        Returns:
            Token object containing access and refresh tokens
        """
        access_token = utils.create_access_token(
            data={"sub": str(user_id)}
        )
        refresh_token = utils.create_refresh_token(
            data={"sub": str(user_id)}
        )
        return schemas.Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
