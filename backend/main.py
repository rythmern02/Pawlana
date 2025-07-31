# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from dotenv import load_dotenv

from supabase_client import supabase
from pet_routes import router as pet_router
from thinker import start_pet_thinker
from wallet_auth import router as wallet_auth_router
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()  # ✅ load .env

app = FastAPI()
auth_scheme = HTTPBearer(auto_error=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    if not cred or cred.scheme.lower() != "bearer":
        raise HTTPException(401, "Missing token")

    try:
        payload = jwt.decode(
            cred.credentials,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )
        return payload
    except jwt.PyJWTError as e:
        raise HTTPException(401, f"Invalid token: {str(e)}")

@app.get("/", tags=["Root"])
async def read_root():
  return { 
    "message": "Welcome to my notes application, use the /docs route to proceed"
   }

# ✅ Route registration (no global Depends)
app.include_router(pet_router, prefix="/pet")
app.include_router(wallet_auth_router)
# ✅ Start thinker
start_pet_thinker(app, supabase)
