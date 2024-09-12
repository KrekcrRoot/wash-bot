from dotenv import load_dotenv
import httpx

import os 
load_dotenv()


class API:

    host = f"{os.environ.get("BACKEND_ADDRESS")}:{os.environ.get("BACKEND_PORT")}"

    def __init__(self):
        pass

    async def get_status(self):
        return httpx.get(f"{self.host}/status")

    