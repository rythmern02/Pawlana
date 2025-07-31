import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def get_pet_path(user_id, pet_id):
    return f"data/users/{user_id}_{pet_id}.json"

def load_pet(user_id, pet_id):
    path = get_pet_path(user_id, pet_id)
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def save_pet(user_id, pet_id, data):
    path = get_pet_path(user_id, pet_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def generate_pet_reply(system_prompt: str, user_message: str) -> str:
    from openai import OpenAI
    import os

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.getenv("NVIDIA_API_KEY")
    )

    completion = client.chat.completions.create(
        model="nvidia/llama-3.3-nemotron-super-49b-v1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.6,
        top_p=0.95,
        max_tokens=4096,
        frequency_penalty=0,
        presence_penalty=0
    )

    return completion.choices[0].message.content


def chat_with_pet(user_id, pet_id, user_input):
    pet = load_pet(user_id, pet_id)
    if not pet:
        return f"No pet found with ID '{pet_id}' for user '{user_id}'"

    name = pet["name"]
    type_ = pet["type"]
    traits = pet.get("traits", [])
    commands = pet.get("commands", [])
    trained_words = pet.get("trained_words", [])
    history = pet.get("history", [])

    system_prompt = f"""
You are {name}, a virtual {type_}.
Traits: {', '.join(traits)}.
Commands: {', '.join(commands)}.
User has trained you on: {', '.join(trained_words)}.
You are emotionally tuned to the user. Reply with personality.
Recent user messages: {[h['message'] for h in history[-3:]]}
"""

    print("🧠 SYSTEM PROMPT:", system_prompt)

    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.3-nemotron-super-49b-v1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.6,
            top_p=0.95,
            max_tokens=1024,
            stream=True
        )

        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
        print("🐶 PET:", full_response)

        pet["history"].append({"message": user_input, "response": full_response})
        save_pet(user_id, pet_id, pet)

        return full_response

    except Exception as e:
        print("❌ ERROR:", str(e))
        return "Oops! The pet is currently unavailable."
