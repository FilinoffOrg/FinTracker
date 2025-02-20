from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

class UserLoginSchema(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(credentials: UserLoginSchema, response: Response):
    if credentials.username == "admin" and credentials.password == "admin":
        token = security.create_access_token(uid="admin")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, value=token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "This is a protected route"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)