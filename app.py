from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import re

port = 8000
app = FastAPI()

def json_to_markdown(data, level=0):
    markdown = ""
    indent = "  " * level
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                markdown += f"{indent}## {key}:\n"
                markdown += json_to_markdown(value, level + 1)
            else:
                markdown += f"{indent}## {key}: {value}\n"
            markdown += "\n"
            
    elif isinstance(data, list):
        for item in data:
            markdown += f"{indent}- "
            if isinstance(item, (dict, list)):
                markdown += "\n" + json_to_markdown(item, level + 1)
            else:
                markdown += f"{item}\n"
                
    return markdown

def markdown_to_json(markdown_text):
    result = {}
    current_key = None
    list_items = []
    
    lines = [line.strip() for line in markdown_text.split('\n') if line.strip()]
    
    for line in lines:
        if line.startswith('##'):
            if current_key and list_items:
                result[current_key] = list_items
                list_items = []
            
            header_match = re.match(r'##\s+(.+?):\s*(.*)$', line)
            if header_match:
                current_key = header_match.group(1)
                value = header_match.group(2)
                if value:
                    result[current_key] = value.strip()
                else:
                    list_items = []
        
        elif line.startswith('-'):
            item = line[1:].strip()
            if item:
                list_items.append(item)
    
    if current_key and list_items:
        result[current_key] = list_items
    
    return result

@app.post("/convert/to-markdown")
async def convert_to_markdown(json_input: dict):
    try:
        markdown = json_to_markdown(json_input)
        return {"markdown": markdown}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/convert/to-json")
async def convert_to_json(markdown_input: dict):
    try:
        json_output = markdown_to_json(markdown_input["markdown"])
        return json_output
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=port)