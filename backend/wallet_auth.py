from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os

router = APIRouter()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class WalletUserCreate(BaseModel):
    wallet_address: str
    username: str
    email: str

@router.post("/wallet-login")
def wallet_login(payload: WalletUserCreate):
    # Check if user already exists
    existing = (
        supabase.table("wallet_users")
        .select("*")
        .eq("wallet_address", payload.wallet_address)
        .execute()
    )

    if existing.data:
        return {"message": "User already exists", "user": existing.data[0]}

    # Insert new user
    result = (
        supabase.table("wallet_users")
        .insert({
            "wallet_address": payload.wallet_address,
            "username": payload.username,
            "email": payload.email,
        })
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=500, detail="Insert failed or returned no data.")

# Optional: log the result
    print("User inserted:", result.data)

    return {"status": "success", "data": result.data}