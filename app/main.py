import os
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx
import json
from jinja2 import Environment, FileSystemLoader
import sys
sys.path.append('/claude-engineer')
from claude_engineer import process_prompt, interact_with_home_assistant

app = FastAPI()

# Load configuration
with open('/data/options.json') as config_file:
    config = json.load(config_file)

CLAUDE_API_KEY = config['claude_api_key']
HOMEASSISTANT_API_KEY = config['homeassistant_api_key']
CLAUDE_MODEL = config['claude_model']

# Set up Jinja2 template environment
template_env = Environment(loader=FileSystemLoader('templates'))

@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    template = template_env.get_template('chat.html')
    return template.render()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        user_message = json.loads(data)['message']
        
        # Process the message with Claude Engineer
        claude_response = process_prompt(user_message, CLAUDE_API_KEY, CLAUDE_MODEL)

        # Check if we need to interact with Home Assistant
        if "modify Home Assistant" in user_message.lower():
            ha_response = interact_with_home_assistant(user_message, HOMEASSISTANT_API_KEY)
            claude_response += f"\n\nHome Assistant: {ha_response}"

        await websocket.send_text(json.dumps({"message": claude_response}))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)