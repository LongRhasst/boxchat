from app.modules.Users import router as auth_router
from app.modules.Messenger import messenger_router as app_router
from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.swagger.swagger import custom_openapi
from app.Cores.middleware import AuthMiddleware
app = FastAPI()
app.openapi = lambda: custom_openapi(app)
app.add_middleware(AuthMiddleware)
app.include_router(auth_router)
app.include_router(app_router)

