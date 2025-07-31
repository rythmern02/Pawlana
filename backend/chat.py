from fastapi import APIRouter
from pydantic import BaseModel
from ai_logic import get_pet_response

router = APIRouter()

class ChatRequest(BaseModel):
    pet_id: str
    message: str

@router.post("/")
async def chat_with_pet(payload: ChatRequest):
    print(f"📨 Incoming message: {payload.message} for pet: {payload.pet_id}")
    reply = get_pet_response(payload.pet_id, payload.message)
    return {"reply": reply}
