import os
from dotenv import load_dotenv

load_dotenv(".env.local")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/karockfe")
POOL_SIZE = os.getenv("POOL_SIZE", "10")
MAX_POOL_SIZE = int(os.getenv("MAX_POOL_SIZE", "15"))
