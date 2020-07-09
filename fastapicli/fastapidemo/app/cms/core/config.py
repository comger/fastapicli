import os


try:
    from pathlib import Path
    from dotenv import load_dotenv
    for p in Path("../").rglob('*dev.env'):
        load_dotenv(dotenv_path=p)
except Exception:
    pass



def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result


DEBUG = getenv_boolean("DEBUG", True)
API_V1_STR = "/api/v1"
LOGIN_API = os.getenv('LOGIN_API', '/api/v1/login/access-token')
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", 1024 * 1024 * 100))
LOG_MAX_NUM = int(os.getenv("LOG_MAX_NUM", 8))

ALGORITHM = os.getenv("ALGORITHM", 'HS256')
SECRET_KEY = os.getenv("SECRET_KEY", "smartbow")

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8
SERVER_NAME = os.getenv("SERVER_NAME", 'localhost')
SERVER_HOST = os.getenv("SERVER_HOST")
BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", "*")
PROJECT_NAME = os.getenv("PROJECT_NAME", "Web Server")

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "192.168.111.147")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", '123456')
POSTGRES_DB = os.getenv("POSTGRES_DB", 'democms')


FIRST_USER = os.getenv("FIRST_USER", "admin")
FIRST_USER_PASSWORD = os.getenv("FIRST_USER_PASSWORD", "admin")


CLIENT_ID = os.getenv("CLIENT_ID", "17da3dda-f3c6-11e9-b4d1-0242ac170002")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "17dce0d0-f3c6-11e9-b4d1-0242ac170002")
USERCENTER_HOST = os.getenv("USERCENTER_HOST", "http://ucapi.sb2.org")
