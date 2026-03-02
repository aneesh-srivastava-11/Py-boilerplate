from .models import User

def create_user(*, email: str, password: str, first_name: str = '', last_name: str = '') -> User:
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    return user
