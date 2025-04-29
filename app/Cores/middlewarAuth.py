from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
import jwt
from app.Cores.config import SECRET_KEY

public_routes = ("/public", "/docs", "/openapi.json", "/redoc", "/auth")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path

        # Bỏ qua các route không yêu cầu bảo mật (public routes)


        if any(path.startswith(route) for route in public_routes):
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

        # Tiếp tục xử lý request
        return await call_next(request)
