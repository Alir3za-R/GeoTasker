from fastapi import APIRouter, Depends, HTTPException, status
# import jwt
from app.schemas.users import UserCreate, Token, UserLogin
from app.crud.users import create_user, get_user_by_email
from app.core.db import get_db
from app.core.security import verify_password, create_login_tokens
from sqlalchemy.orm import Session
router = APIRouter(prefix="/users")

@router.post("/create/", tags=["users"])
async def create_user_api(user_data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db=db, user=user_data)
    return {"message": f"User {user.first_name} {user.last_name} was created successfully!",}

@router.post("/login/", response_model=Token, tags=["users"])
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_credentials.email)
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return create_login_tokens(user=user)

# TODO: complete refresh token api
# @router.post("/token/refresh", response_model=Token, tags=["users"])
# async def refresh_token(refresh_token: str):
#     try:
#         payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_id = payload.get("sub")
#         if not user_id:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

#     access_token = create_access_token(data={"sub": user_id})
#     new_refresh_token = create_refresh_token(data={"sub": user_id})

#     return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

