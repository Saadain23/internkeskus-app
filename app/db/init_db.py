# app/db/init_db.py

from app.db.mongodb import db
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.core.config import settings

async def init_db():
    # Create indices
    db_name = settings.PROJECT_NAME
    await db.client[db_name].users.create_index("email", unique=True)
    await db.client[db_name].student_profiles.create_index("user_id", unique=True)
    await db.client[db_name].recruiter_profiles.create_index("user_id", unique=True)

    # Seed initial data if necessary
    admin_email = "admin@internkeskus.com"
    existing_admin = await db.client[db_name].users.find_one({"email": admin_email})

    if not existing_admin:
        admin_user = User(
            email=admin_email,
            hashed_password=get_password_hash("adminpassword"),
            is_active=True,
            role=UserRole.ADMIN
        )
        await db.client[db_name].users.insert_one(admin_user.dict())
        print("Admin user created.")
    else:
        print("Admin user already exists.")
