from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(hashed_password: str, plain_password: str) -> bool:
    return pwd_context.verify(hashed_password, plain_password)
