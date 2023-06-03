import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.curdir, '.env'))

SQLACHEMY_DATABASE_URL = os.environ.get("DB_URL", "")

SECRET_KEY = os.environ.get("SECRET_KEY", "")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", ""))