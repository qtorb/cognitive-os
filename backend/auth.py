"""
Authentication module for Cognitive OS
Handles Google OAuth 2.0 and JWT token management
"""

from datetime import datetime, timedelta
from typing import Optional
import os
import json
import requests
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User

# Configuration from environment
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth/callback")

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24 * 7  # 7 days


def create_jwt_token(user_id: str, email: str) -> str:
    """Create JWT token for authenticated user"""
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("user_id")
        email: str = payload.get("email")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return {"user_id": user_id, "email": email}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def get_google_token(code: str) -> dict:
    """Exchange authorization code for Google access token"""
    token_url = "https://oauth2.googleapis.com/token"

    payload = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=payload)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get Google token"
        )

    return response.json()


def get_google_user_info(access_token: str) -> dict:
    """Get user info from Google using access token"""
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get Google user info"
        )

    return response.json()


def process_google_login(code: str, db: Session) -> dict:
    """
    Process Google OAuth login:
    1. Exchange code for token
    2. Get user info
    3. Create or update user in DB
    4. Return JWT token
    """

    # Get access token from Google
    token_data = get_google_token(code)
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No access token from Google"
        )

    # Get user info from Google
    google_user = get_google_user_info(access_token)

    google_id = google_user.get("id")
    email = google_user.get("email")
    name = google_user.get("name")
    picture = google_user.get("picture")

    if not email or not google_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Google user data"
        )

    # Find or create user
    user = db.query(User).filter(User.email == email).first()

    if not user:
        # Create new user
        import uuid
        user_id = str(uuid.uuid4())
        user = User(
            user_id=user_id,
            email=email,
            google_id=google_id,
            name=name,
            picture_url=picture,
            onboarded=0
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update existing user with Google info
        user.google_id = google_id
        user.name = name
        user.picture_url = picture
        db.commit()
        db.refresh(user)

    # Create JWT token
    jwt_token = create_jwt_token(user.user_id, user.email)

    return {
        "token": jwt_token,
        "user_id": user.user_id,
        "email": user.email,
        "name": user.name,
        "onboarded": bool(user.onboarded)
    }


def get_current_user(token: str, db: Session) -> User:
    """Get current authenticated user from JWT token"""
    token_data = verify_jwt_token(token)
    user = db.query(User).filter(User.user_id == token_data["user_id"]).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
