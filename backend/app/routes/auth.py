from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from contextlib import asynccontextmanager
import uuid
import asyncio

from app.database import get_session
from app.models import User
from app.schemas import AuthRequest, AuthResponse, UserResponse
from app.utils.jwt import create_access_token
from app.utils.password import hash_password, verify_password
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    data: AuthRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Create a new user account."""
    print(f"DEBUG: Signup attempt for {data.email}")
    # Check if email already exists
    statement = select(User).where(User.email == data.email)
    result = await session.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        print(f"DEBUG: Email {data.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(data.password)

    user = User(
        id=user_id,
        email=data.email,
        password_hash=hashed_password,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    print(f"DEBUG: User created: {user.id}")

    # Create JWT token
    token = create_access_token(user.id, user.email)
    print(f"DEBUG: Token created for {user.id}")

    # Set cookie
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )

    return AuthResponse(
        user=UserResponse(id=user.id, email=user.email, name=user.name),
        token=token
    )


@router.post("/signin", response_model=AuthResponse)
async def signin(
    data: AuthRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    """Sign in with email and password."""
    print(f"DEBUG: Signin attempt for {data.email}")

    try:
        # Find user
        statement = select(User).where(User.email == data.email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        print(f"DEBUG: User found: {user is not None}")

        if not user:
            print(f"DEBUG: User not found for {data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(data.password, user.password_hash):
            print(f"DEBUG: Password verification failed for {data.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        print(f"DEBUG: Password verified for {data.email}")

        # Create JWT token
        token = create_access_token(user.id, user.email)
        print(f"DEBUG: Token created for {user.id}")

        # Set cookie
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=60 * 60 * 24 * 7,  # 7 days
        )

        print(f"DEBUG: Cookie set, returning user")
        return AuthResponse(
            user=UserResponse(id=user.id, email=user.email, name=user.name),
            token=token
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Signin error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during signin",
        )


@router.post("/signout")
async def signout(
    response: Response,
    current_user: dict = Depends(get_current_user),
):
    """Sign out and clear the auth cookie."""
    response.delete_cookie(key="auth_token")
    return {"message": "Signed out successfully"}


@router.get("/session", response_model=AuthResponse)
async def get_session_route(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Get the current user session."""
    user_id = current_user.get("sub")

    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Create a fresh token for the session check
    token = create_access_token(user.id, user.email)

    return AuthResponse(
        user=UserResponse(id=user.id, email=user.email, name=user.name),
        token=token
    )
