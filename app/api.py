from dotenv import load_dotenv
import httpx

import os 
load_dotenv()

HEADERS = {}

class API:

    host = f"{os.environ.get("BACKEND_ADDRESS")}:{os.environ.get("BACKEND_PORT")}"

    def __init__(self):
        pass

    async def get_my(self, user_id):
        return httpx.get(f"{self.host}/user/my", headers={
            'Authorization': str(user_id)
        })

    async def get_status(self):
        return httpx.get(f"{self.host}/status", headers={
            'Content-Type': 'application/json'
        })
    
    async def get_users(self):
        return httpx.get(f"{self.host}/")
    
    async def auth(self, user_tag, user_id):
        return httpx.post(f"{self.host}/user/auth", json={
            "telegram_tag": f"@{user_tag}",
            "telegram_id": str(user_id)
        })


def init_api_controller():
    return API()