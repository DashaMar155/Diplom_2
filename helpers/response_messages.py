from enum import Enum


class UserError(Enum):
    DUPLICATE = "User already exists"
    MISSING_FIELDS = "Email, password and name are required fields"


class AuthError(Enum):
    INVALID_CREDENTIALS = "email or password are incorrect"


class OrderError(Enum):
    MISSING_INGREDIENTS = "Ingredient ids must be provided"
    INVALID_HASH = "Internal Server Error"
