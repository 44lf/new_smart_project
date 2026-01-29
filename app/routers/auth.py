from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.core.exceptions import AppError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import TokenOut, UserCreate, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_db)) -> UserOut:
    repo = UserRepository(session)
    existing = await repo.get_by_username(payload.username)
    if existing:
        raise AppError(400, "Username already exists")
    user = User(username=payload.username, password_hash=hash_password(payload.password), role="user")
    saved = await repo.create(user)
    return UserOut(id=saved.id, username=saved.username, role=saved.role)


@router.post("/login", response_model=TokenOut)
async def login(payload: UserCreate, session: AsyncSession = Depends(get_db)) -> TokenOut:
    repo = UserRepository(session)
    user = await repo.get_by_username(payload.username)
    if not user or not verify_password(payload.password, user.password_hash):
        raise AppError(401, "Invalid credentials")
    token = create_access_token(str(user.id))
    return TokenOut(access_token=token)
