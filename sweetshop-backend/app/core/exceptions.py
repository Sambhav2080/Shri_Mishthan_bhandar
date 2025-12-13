from fastapi import HTTPException,status

class UserAlreadyExistsException(HTTPException):
    def __init__(self,email:str):
        super().__init__(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"User with email '{email}' already exists."
        )

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password."
        )

class SweetNotFound(Exception):
    """Sweet does not exist in database."""
    pass

class OutOfStock(Exception):
    """Cannot purchase because quantity is zero."""
    pass

class UnauthorizedAction(Exception):
    """Action for admin only."""
    pass


