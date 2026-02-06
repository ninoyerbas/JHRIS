"""
Authentication API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_active_user
from app.auth import schemas, service
from app.users import schemas as user_schemas
from app.users import service as user_service

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: schemas.RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        user_in: Registration data
        db: Database session
        
    Returns:
        Created user object
        
    Raises:
        HTTPException: If email already registered
    """
    # Check if user already exists
    existing_user = user_service.UserService.get_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = user_service.UserService.create(
        db,
        user_schemas.UserCreate(email=user_in.email, password=user_in.password)
    )
    return user


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password to get access token.
    
    Args:
        form_data: Login credentials
        db: Database session
        
    Returns:
        Access and refresh tokens
        
    Raises:
        HTTPException: If credentials are invalid
    """
    user = service.AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return service.AuthService.create_tokens(user.id)


@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    current_user: user_schemas.User = Depends(get_current_active_user),
):
    """
    Refresh access token using a valid refresh token.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        New access and refresh tokens
    """
    return service.AuthService.create_tokens(current_user.id)


@router.get("/me", response_model=user_schemas.User)
async def get_current_user_info(
    current_user: user_schemas.User = Depends(get_current_active_user),
):
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user object
    """
    return current_user
