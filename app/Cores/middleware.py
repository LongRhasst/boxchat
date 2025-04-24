from fastapi import Request, Depends
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.Cores.config import SECRET_KEY

http_bearer = HTTPBearer(auto_error=False)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path

        # Bỏ qua các route public và docs
        if path.startswith(("/public", "/docs", "/openapi.json", "/redoc")):
            return await call_next(request)

        # Chỉ kiểm tra token với route /user
        if path.startswith("/user"):
            credentials: HTTPAuthorizationCredentials = await http_bearer(request)
            if not credentials or credentials.scheme.lower() != "bearer":
                return JSONResponse({"message": "Unauthorized"}, status_code=401)

            token = credentials.credentials
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                request.state.user_id = payload.get("user_id")
            except jwt.ExpiredSignatureError:
                return JSONResponse({"message": "Token Expired"}, status_code=401)
            except jwt.InvalidTokenError:
                return JSONResponse({"message": "Invalid Token"}, status_code=401)

        return await call_next(request)
