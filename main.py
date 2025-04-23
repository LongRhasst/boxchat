from fastapi import FastAPI
from app.modules.Router import router as auth_router
from app.database import boxchat
from app.Cores.database import engine
app = FastAPI()

app.include_router(auth_router)
boxchat.Base.metadata.create_all(bind = engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

#migration, model
#dùng alchemy tạo 2 models: sinh_vien, lop_hoc (id, name)
#tạo migration tạo ra 2 bảng
#fastapi viết crud cho 2 bảng này
