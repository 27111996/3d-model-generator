from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import re
import base64
from datetime import datetime
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class PromptRequest(BaseModel):
    prompt: str

def generate_scad(prompt: str) -> str:
    system_prompt = """You are an OpenSCAD code generator.
STRICT RULES:
1. Output ONLY valid OpenSCAD code
2. NO explanations, NO comments, NO markdown
3. Start directly with OpenSCAD syntax
4. Use only numbers, NO units like mm or cm
5. Example output: sphere(r=15);
Generate OpenSCAD code for: """ + prompt

    result = subprocess.run(
        ["ollama", "run", "qwen2.5-coder:1.5b", system_prompt],
        capture_output=True, text=True
    )
    code = result.stdout.strip()
    
    # Remove markdown
    code = re.sub(r'```[a-zA-Z]*', '', code)
    code = code.replace('```', '').strip()
    
    # Remove mm/cm units
    code = re.sub(r'(\d+)(mm|cm|m|in)', r'\1', code)
    
    # Find start of actual code
    for keyword in ['module','cube','cylinder','sphere','union','difference','translate','rotate','linear_extrude']:
        if keyword in code:
            code = code[code.find(keyword):]
            break
    
    # Remove trailing explanation
    lines = []
    for line in code.split('\n'):
        if any(line.strip().startswith(w) for w in ['This','The ','Note','Here','In ','You','It ']):
            break
        lines.append(line)
    
    return '\n'.join(lines).strip()

@app.post("/generate")
async def generate(request: PromptRequest):
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    scad_path = f"/home/sandra/3d_model_generator/models/{name}.scad"
    png_path = f"/home/sandra/3d_model_generator/outputs/{name}.png"
    
    scad_code = generate_scad(request.prompt)
    
    with open(scad_path, "w") as f:
        f.write(scad_code)
    
    result = subprocess.run(
        ["openscad","--imgsize=800,600","--autocenter","--viewall","-o",png_path,scad_path],
        capture_output=True, text=True
    )
    
    if not os.path.exists(png_path):
        return {"error": "Render failed", "scad_code": scad_code, "openscad_error": result.stderr}
    
    with open(png_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()
    
    return {"scad_code": scad_code, "image": img_base64, "status": "success"}

@app.get("/")
async def root():
    return {"message": "3D Model Generator API Running!"}
