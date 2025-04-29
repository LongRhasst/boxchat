from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI
from app.Cores.middlewarAuth import public_routes

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My Custom API",
        version="1.0.0",
        description="This is a custom API with Bearer Auth",
        routes=app.routes,
    )

    # Thêm security schema cho HTTP Bearer
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Lọc các route không phải public route và chỉ thêm security vào các route này
    for path, path_item in openapi_schema["paths"].items():
        # Kiểm tra nếu route không phải là public route
        if not any(path.startswith(prefix) for prefix in public_routes):
            for method in path_item.values():
                # Thêm security vào mỗi method (GET, POST, PUT, DELETE, v.v.)
                method.setdefault("security", [{"HTTPBearer": []}])

    # Lưu OpenAPI schema đã cập nhật vào app
    app.openapi_schema = openapi_schema

    return app.openapi_schema
