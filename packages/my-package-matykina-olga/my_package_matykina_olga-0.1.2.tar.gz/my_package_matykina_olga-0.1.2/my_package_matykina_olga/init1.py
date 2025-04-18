# my_package/__init__.py
from .database import connect, _internal_function
from .user_management import create_user

__all__ = ['connect', 'create_user', '_internal_function']
