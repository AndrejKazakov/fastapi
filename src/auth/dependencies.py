from jwt.exceptions import InvalidTokenError

from fastapi import (
    Form,
    HTTPException,
    status,
    Depends,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from auth import utils as auth_utils
from users.schemas import UserSchema

http_bearer = HTTPBearer()


john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("123"),
    email="sam@example.com",
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user_login(
    username: str = Form(),
    password: str = Form(),
):
    unauth_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )

    if not (user := users_db.get(username)):
        raise unauth_ex
    if not auth_utils.validate_password(
        password,
        user.password,
    ):
        raise unauth_ex
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user invactive",
        )

    return user


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> UserSchema:
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )
