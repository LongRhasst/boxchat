from fastapi import Request
from pygments.lexers.templates import JspLexer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
import jwt
from app.Cores.config import SECRET_KEY, REFRESH_KEY

public_routes = ("/public", "/docs", "/openapi.json", "/redoc", "/auth")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path

        # Bỏ qua các route không yêu cầu bảo mật (public routes)

        if any(path.startswith(route) for route in public_routes):
            return await call_next(request)

        # 👉 Lấy token từ cookies thay vì header
        token = request.headers.get("Authorization")

        if not token:
            return JSONResponse({"message": "Unauthorized - Missing Token"}, status_code=401)
        token = token.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = request.state.user_id = payload.get("id")
            if user_id is None:
                return JSONResponse({"message": "Unauthorized - User ID Not F   ound"}, status_code=401)
        except jwt.ExpiredSignatureError:
            refreshed_token = request.cookies.get("refresh_token")
            payload = jwt.decode(refreshed_token, REFRESH_KEY, algorithms=["HS256"])
            user_id = payload.get("id")

            from app.modules.Users import db_dependency, create_access_token
            from app.database.boxchat import User
            user_email = db_dependency.query(User).filter(User.id == user_id).first().email
            access_token = create_access_token(user_id, user_email)
            response = JSONResponse({"message": "Token Is Refresh"}, status_code=200)
            response.headers["Authorization"] = f"Bearer {access_token}"
            return response
        except jwt.InvalidTokenError:
            return JSONResponse({"message": "Invalid Token"}, status_code=401)

        # Tiếp tục xử lý request
        return await call_next(request)
