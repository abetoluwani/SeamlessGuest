from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
import uvicorn
import os
from dotenv import load_dotenv
from tools import tools

# Load environment variables
load_dotenv()

app = FastAPI()

@app.get("/cmnd-tools")
def cmnd_tools_endpoint():
    tools_response = [
        {
            "name": tool["name"],
            "description": tool["description"],
            "jsonSchema": tool["parameters"],
            "isDangerous": tool.get("isDangerous", False),
            "functionType": tool["functionType"],
            "isLongRunningTool": tool.get("isLongRunningTool", False),
            "rerun": tool["rerun"],
            "rerunWithDifferentParameters": tool["rerunWithDifferentParameters"],
        } for tool in tools
    ]
    return JSONResponse(content={"tools": tools_response})

@app.post("/run-cmnd-tool")
async def run_cmnd_tool_endpoint(request: Request):
    data = await request.json()
    tool_name = data.get('toolName')
    props = data.get('props', {})
    tool = next((t for t in tools if t['name'] == tool_name), None)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    try:
        result = await tool["runCmd"](**props)
        return JSONResponse(content=result, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8888)
