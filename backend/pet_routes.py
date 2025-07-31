from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from supabase_client import supabase
from ai_logic import generate_pet_reply
from typing import Optional
from jwt_utils import get_current_user
import json 

router = APIRouter()

# -------------------------------
# 📦 Pydantic Models
# -------------------------------

class CreatePetRequest(BaseModel):
    pet_name: str
    pet_type: str

class ChatRequest(BaseModel):
    pet_id: str
    message: str

class TrainRequest(BaseModel):
    pet_id: str
    command: str
    response: str

# -------------------------------
#  Create a Pet
# -------------------------------
@router.post("/create")
async def create_pet(req: CreatePetRequest, user=Depends(get_current_user)):
    data = {
        "user_id": user["sub"],
        "name": req.pet_name,
        "type": req.pet_type,
        "traits": ["curious", "friendly"],
        "commands": ["sit", "roll"],
        "trained_words": [],
        "wallet_address": None
    }

    result = supabase.table("pets").insert(data).execute()

    # if result.status_code != 201:
    #     raise HTTPException(status_code=500, detail="Failed to create pet")

    return {"message": "Pet created successfully", "pet": result.data[0]}

# -------------------------------
# Chat With Pet
# -------------------------------

@router.post("/chat")
async def chat(payload: ChatRequest, user=Depends(get_current_user)):
    pet_data = supabase.table("pets")\
        .select("*")\
        .eq("id", payload.pet_id)\
        .eq("user_id", user["sub"])\
        .single()\
        .execute()

    # if pet_data.error or pet_data.data is None:
    #     raise HTTPException(status_code=404, detail="Pet not found")

    pet = pet_data.data

    # Fetch last 3 messages for memory (optional)
    messages_result = supabase.table("messages")\
        .select("*")\
        .eq("pet_id", payload.pet_id)\
        .order("timestamp", desc=True)\
        .limit(3)\
        .execute()

    history = messages_result.data if messages_result.data else []

    reply = generate_pet_reply(
    "You're a pet in Petoverse. You can only speak in cute and short sentences. "
    "Your responses are emotionally intelligent " + json.dumps(pet) +
    " and context-aware. and you have this history " + json.dumps(history),
    payload.message
)
    # Store messages (user + pet reply)
    supabase.table("messages").insert([
        {
            "pet_id": payload.pet_id,
            "role": "user",
            "content": payload.message
        },
        {
            "pet_id": payload.pet_id,
            "role": "pet",
            "content": reply
        }
    ]).execute()

    return {"reply": reply}

# -------------------------------
# Train Pet
# -------------------------------

@router.post("/train")
async def train(payload: TrainRequest, user=Depends(get_current_user)):
    pet_data = supabase.table("pets")\
        .select("*")\
        .eq("id", payload.pet_id)\
        .eq("user_id", user["sub"])\
        .single()\
        .execute()

    if pet_data.error or pet_data.data is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet = pet_data.data

    updated_commands = list(set(pet.get("commands", []) + [payload.command]))
    updated_words = list(set(pet.get("trained_words", []) + [payload.command]))

    updates = {
        "commands": updated_commands,
        "trained_words": updated_words
    }

    supabase.table("pets")\
        .update(updates)\
        .eq("id", payload.pet_id)\
        .execute()

    # Optional: log training (if you have a `training_logs` table)

    return {"message": "Pet trained successfully with new command."}
