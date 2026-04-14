import requests
import json
from http.server import BaseHTTPRequestHandler
import os

# Configuration
GITHUB_PAT = os.environ.get("GITHUB_PAT") # Put your token in Vercel Env Vars
CS_NAME = "glorious-goggles-wr5gj9rq5j69h9wqw" 

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        headers = {"Authorization": f"Bearer {GITHUB_PAT}"}
        
        # 1. Check current status
        status_url = f"https://api.github.com/user/codespaces/{CS_NAME}"
        res = requests.get(status_url, headers=headers).json()
        
        # 2. If it's not 'Available', wake it up
        if res.get("state") != "Available":
            start_url = f"https://api.github.com/user/codespaces/{CS_NAME}/start"
            requests.post(start_url, headers=headers)
            return self.send_json({"output": "Codespace was asleep. Waking it up... Please wait 20 seconds."})

        # 3. If it is awake, forward the command to your listener.py
        # (Same forwarding logic as before...)
