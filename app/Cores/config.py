import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("MYSQL_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_KEY = os.getenv("REFRESH_KEY")
