# thinker.py

import asyncio
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

# background loop
async def thinker_loop(supabase):
    print("🧠 Thinker loop started")
    while True:
        try:
            pets = supabase.table("pets").select("*").execute().data
            for pet in pets:
                # Sample logic to decide something for a pet
                prompt = f"You are {pet['name']} the {pet['type']}. What should I notify your owner today?"
                completion = client.chat.completions.create(
                    model="nvidia/llama-3.3-nemotron-super-49b-v1",
                    messages=[
                        {"role": "system", "content": "You're a smart pet agent that cares for the user."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=256
                )
                thought = completion.choices[0].message.content

                supabase.table("notifications").insert({
                    "pet_id": pet["id"],
                    "message": thought
                }).execute()

        except Exception as e:
            print("❌ Thinker error:", e)
            
        break # 1-hour interval

# Entry point
def start_pet_thinker(app, supabase):
    @app.on_event("startup")
    async def launch_thinker():
        asyncio.create_task(thinker_loop(supabase))
