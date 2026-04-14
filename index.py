from http.server import BaseHTTPRequestHandler
import requests
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. Get the command from your webpage request
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        user_command = post_data.get("command", "echo 'No command provided'")

        # 2. Setup your Codespace details
        # Replace 'YOUR-CODESPACE-NAME' with your actual name
        codespace_name = "supreme-space-umbrella-x4v" 
        listener_url = f"https://{codespace_name}-5000.app.github.dev/run"

        # 3. Forward the command to the Codespace
        try:
            response = requests.post(
                listener_url, 
                json={"command": user_command},
                timeout=10
            )
            output = response.text
        except Exception as e:
            output = f"Error: {str(e)}"

        # 4. Send the terminal output back to your webpage
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"terminal_output": output}).encode())
