from fastapi import (
    APIRouter,
    Depends,
)

from users.schemas import UserSchema
from auth import utils as auth_utils

from .schemas import TokenInfo
from .dependencies import (
    validate_auth_user_login,
    get_current_active_auth_user,
)

router = APIRouter(prefix="/jwt", tags=["JWT"])


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user_login),
):
    # TODO: COOKIES
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }

    token = auth_utils.encode_jwt(
        jwt_payload,
    )
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/users/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_active_auth_user),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
