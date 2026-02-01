from sqlmodel import SQLModel, create_engine
import os
import sys

# Add the current directory to sys.path to find 'app'
sys.path.append(os.getcwd())

from app.models.task import Task
from app.models.user import User
from app.config import get_settings

settings = get_settings()
print(f"Connecting to: {settings.database_url}")

# We use the sync engine for schema creation (easier)
sync_url = settings.database_url.replace("+aiosqlite", "")
engine = create_engine(sync_url)

print("Creating tables...")
SQLModel.metadata.create_all(engine)
print("Tables created successfully!")
