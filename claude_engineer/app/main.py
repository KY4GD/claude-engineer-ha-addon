import os
import logging
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import json
from jinja2 import Environment, FileSystemLoader
import sys
import asyncio
sys.path.append('/claude-engineer')
from claude_engineer import process_prompt, interact_with_home_assistant

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Load configuration
try:
    with open('/data/options.json') as config_file:
        config = json.load(config_file)
    
    CLAUDE_API_KEY = config['claude_api_key']
    HOMEASSISTANT_API_KEY = config['homeassistant_api_key']
    CLAUDE_MODEL = config['claude_model']
except Exception as e:
    logger.error(f"Failed to load configuration: {str(e)}")
    raise

# Set up Jinja2 template environment
template_env = Environment(loader=FileSystemLoader('templates'))

@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    try:
        template = template_env.get_template('chat.html')
        return template.render()
    except Exception as e:
        logger.error(f"Error rendering chat page: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            user_message = json.loads(data)['message']
            
            # Process the message with Claude Engineer
            claude_response = await process_prompt(user_message, CLAUDE_API_KEY, CLAUDE_MODEL)

            # Check if we need to interact with Home Assistant
            if "modify Home Assistant" in user_message.lower():
                ha_response = await interact_with_home_assistant(user_message, HOMEASSISTANT_API_KEY)
                claude_response += f"\n\nHome Assistant: {ha_response}"

            await websocket.send_text(json.dumps({"message": claude_response}))
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close()

async def shutdown():
    logger.info("Shutting down")
    # Implement any necessary cleanup here

if __name__ == "__main__":
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.serve())
    loop.run_until_complete(shutdown())