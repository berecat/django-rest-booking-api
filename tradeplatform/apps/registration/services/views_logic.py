from apps.registration.services.db_interaction import get_user_by_id
from apps.registration.tokens import get_user_id_by_given_token


def reset_user_password(token: str, password: str) -> None:
    """Reset user password by the given JWT token"""

    user_id = get_user_id_by_given_token(token=token)
    user = get_user_by_id(user_id=user_id)
    user.set_password(password)
    user.save()
