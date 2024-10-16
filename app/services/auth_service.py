from app.models.user import User, UserRole
from app.core.security import verify_password, get_password_hash, create_access_token
from app.db.mongodb import db

async def authenticate_user(email: str, password: str):
    user = await db.database.users.find_one({"email": email})
    if user and verify_password(password, user["hashed_password"]):
        return User(**user)
    return False

async def create_user(user_create):
    user_dict = user_create.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["is_active"] = False  # Pending verification
    user = User(**user_dict)
    await db.database.users.insert_one(user.dict())
    # Send verification email logic here
    return user
