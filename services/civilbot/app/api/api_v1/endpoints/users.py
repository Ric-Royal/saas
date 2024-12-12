from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.crud import crud_user
from app.schemas.user import User, UserCreate, UserUpdate, UserPreferenceUpdate
from app.core.security import verify_admin_token

router = APIRouter()

@router.post("/", response_model=User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    admin: bool = Depends(verify_admin_token)
):
    """
    Create new user (admin only)
    """
    user = crud_user.get_by_phone(db, phone_number=user_in.phone_number)
    if user:
        raise HTTPException(
            status_code=400,
            detail="User with this phone number already exists"
        )
    return crud_user.create(db, obj_in=user_in)

@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    admin: bool = Depends(verify_admin_token)
):
    """
    Retrieve users (admin only)
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    admin: bool = Depends(verify_admin_token)
):
    """
    Get user by ID (admin only)
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    admin: bool = Depends(verify_admin_token)
):
    """
    Update user (admin only)
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.put("/{user_id}/preferences", response_model=User)
def update_user_preferences(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    preferences_in: UserPreferenceUpdate,
    admin: bool = Depends(verify_admin_token)
):
    """
    Update user preferences (admin only)
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud_user.update_preferences(db, db_obj=user, preferences_in=preferences_in)
    return user

@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    admin: bool = Depends(verify_admin_token)
):
    """
    Delete user (admin only)
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud_user.remove(db, id=user_id)
    return user 