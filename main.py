from app.modules.Router import router as auth_router
from app.database import boxchat
from app.Cores.database import engine
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(auth_router)
boxchat.Base.metadata.create_all(bind = engine)

@app.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
#migration, model
#dùng alchemy tạo 2 models: sinh_vien, lop_hoc (id, name)
#tạo migration tạo ra 2 bảng
#fastapi viết crud cho 2 bảng này
