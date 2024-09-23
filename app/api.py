from dotenv import load_dotenv
import httpx

import os 
load_dotenv()

HEADERS = {}

class API:

    host = f"{os.environ.get("BACKEND_ADDRESS")}:{os.environ.get("BACKEND_PORT")}"

    def __init__(self):
        pass

    async def get_users(self):
        return httpx.get(f"{self.host}/")
    
    #Interaction with user
    
    async def auth(self, user_tag, user_id):
        return httpx.post(f"{self.host}/user/auth", json={
            "telegram_tag": f"@{user_tag}",
            "telegram_id": str(user_id)
        })
    
    async def user_info(self, user_id):
        return httpx.get(f"{self.host}/user/my", headers={
            'Authorization': str(user_id)
        })
    
    async def admin_check(self, user_id):
        return httpx.get(f"{self.host}/admin/check", headers={
            'Authorization': str(user_id)
        })

    #Interaction with washing
    async def wash_status(self, user_id):
        return httpx.get(f"{self.host}/wash/status", headers={
            'Authorization': str(user_id)
        })
    
    async def wash_occupy(self, user_id):
        return httpx.post(f"{self.host}/wash/occupy", headers={
            'Authorization': str(user_id)
        })
    async def wash_end(self, user_id):
        return httpx.post(f"{self.host}/wash/end", headers={
            'Authorization': str(user_id)
        })
    
    #Interaction with order

    async def order_user(self, user_id):
        return httpx.post(f"{self.host}/order/get-last", headers={
            'Authorization': user_id
        })
    
    #Interaction with machines
    async def get_machines(self):
        return httpx.get(f"{self.host}/machine/all")
    
    async def user_machines(self, user_id):
        return httpx.get(f"{self.host}/machine/my", headers={
            'Authorization': str(user_id)
        })

    async def link_machine(self, user_id, machine_id):
        return httpx.post(f"{self.host}/machine/link", headers={
            'Authorization': str(user_id)
        }, json={
            'uuid': machine_id
        })
    async def unlink_machine(self, user_id):
        return httpx.post(f"{self.host}/machine/unlink", headers={
            'Authorization': str(user_id)
        })

def init_api_controller():
    return API()