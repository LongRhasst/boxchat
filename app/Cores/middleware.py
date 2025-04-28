from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
import jwt
from app.Cores.config import SECRET_KEY

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path

        # Bỏ qua các route public và docs
        if path.startswith(("/public", "/docs", "/openapi.json", "/redoc")):
            return await call_next(request)

        # 👉 Lấy token từ cookies thay vì header
        token = request.cookies.get("access_token")

        if not token:
            return JSONResponse({"message": "Unauthorized - Missing Token"}, status_code=401)

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.state.user_id = payload.get("user_id")
        except jwt.ExpiredSignatureError:
            return JSONResponse({"message": "Token Expired"}, status_code=401)
        except jwt.InvalidTokenError:
            return JSONResponse({"message": "Invalid Token"}, status_code=401)

        return await call_next(request)
