from fastapi import APIRouter, Depends
from ..auth import User as UserSchema, get_current_active_user
from ..utils.debug import debug

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_active_user)):
    debug.log(f"Getting user info for: {current_user.username}")
    return current_user
