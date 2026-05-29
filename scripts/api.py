from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import re
import base64
import glob
from datetime import datetime
import os
from mistralai import Mistral

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- Mistral client ---
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "ZpCcPjCxGnfvSqMTt6SGqTuIxeBfYBmP")
client = Mistral(api_key=MISTRAL_API_KEY)

class PromptRequest(BaseModel):
    prompt: str

class RefineRequest(BaseModel):
    previous_scad: str
    instruction: str

# --- Shape dictionary ---
SHAPES = {
    "chair": """union() {
  translate([0,0,12]) cube([40,40,4], center=true);
  translate([-16,-16,0]) cylinder(h=12, r=2);
  translate([16,-16,0]) cylinder(h=12, r=2);
  translate([-16,16,0]) cylinder(h=12, r=2);
  translate([16,16,0]) cylinder(h=12, r=2);
  translate([0,18,18]) cube([40,4,12], center=true);
}""",
    "table": """union() {
  translate([0,0,25]) cube([60,60,4], center=true);
  translate([-25,-25,0]) cylinder(h=25, r=3);
  translate([25,-25,0]) cylinder(h=25, r=3);
  translate([-25,25,0]) cylinder(h=25, r=3);
  translate([25,25,0]) cylinder(h=25, r=3);
}""",
    "house": """union() {
  cube([40,40,30], center=true);
  translate([0,0,25]) cylinder(h=20, r1=30, r2=0, $fn=4);
}""",
    "snowman": """union() {
  sphere(r=10);
  translate([0,0,17]) sphere(r=8);
  translate([0,0,30]) sphere(r=6);
}""",
    "rocket": """union() {
  cylinder(h=40, r=5);
  translate([0,0,40]) cylinder(h=15, r1=5, r2=0);
  translate([5,0,0]) rotate([0,30,0]) cylinder(h=15, r=1);
  translate([-5,0,0]) rotate([0,-30,0]) cylinder(h=15, r=1);
}""",
    "box": """cube([30,20,10], center=true);""",
    "sphere": """sphere(r=20);""",
    "cylinder": """cylinder(h=30, r=10);""",
    "cone": """cylinder(h=30, r1=15, r2=0);""",
    "mushroom": """union() {
  cylinder(h=20, r=5);
  translate([0,0,25]) sphere(r=18);
}""",
    "trophy": """union() {
  cylinder(h=5, r=15);
  translate([0,0,8]) cylinder(h=20, r=8);
  translate([0,0,31]) sphere(r=8);
}""",
    "cat": """union() {
  sphere(r=10);
  translate([0,0,14]) sphere(r=8);
  translate([-4,0,22]) cylinder(h=6, r1=3, r2=1);
  translate([4,0,22]) cylinder(h=6, r1=3, r2=1);
  translate([15,0,8]) rotate([0,90,0]) cylinder(h=10, r=2);
}""",
    "tree": """union() {
  cylinder(h=15, r=3);
  translate([0,0,15]) cylinder(h=20, r1=15, r2=0);
  translate([0,0,25]) cylinder(h=20, r1=12, r2=0);
  translate([0,0,35]) cylinder(h=15, r1=8, r2=0);
}""",
    "car": """union() {
  cube([60,25,15], center=true);
  translate([0,0,10]) cube([35,22,12], center=true);
  translate([-18,-15,0]) cylinder(h=5, r=8);
  translate([18,-15,0]) cylinder(h=5, r=8);
  translate([-18,15,0]) cylinder(h=5, r=8);
  translate([18,15,0]) cylinder(h=5, r=8);
}""",
    "rectangle": """cube([40,20,5], center=true);""",
    "square": """cube([30,30,5], center=true);""",
    "triangle": """linear_extrude(height=5) polygon(points=[[0,0],[30,0],[15,25]]);""",
    "hexagon": """linear_extrude(height=5) circle(r=20, $fn=6);""",
    "pentagon": """linear_extrude(height=5) circle(r=20, $fn=5);""",
    "ring": """difference() { cylinder(h=5, r=20); cylinder(h=5, r=15); }""",
    "pyramid": """polyhedron(points=[[0,0,0],[30,0,0],[30,30,0],[0,30,0],[15,15,20]], faces=[[0,1,2,3],[0,1,4],[1,2,4],[2,3,4],[3,0,4]]);""",
    "bottle": """union() {
  cylinder(h=30, r=10);
  translate([0,0,30]) cylinder(h=15, r1=10, r2=4);
  translate([0,0,45]) cylinder(h=10, r=4);
}""",
    "robot": """union() {
  translate([0,0,20]) cube([30,20,30], center=true);
  translate([0,0,50]) cube([25,20,25], center=true);
  translate([-20,0,30]) cube([10,10,25], center=true);
  translate([20,0,30]) cube([10,10,25], center=true);
  translate([-8,0,10]) cube([10,10,20], center=true);
  translate([8,0,10]) cube([10,10,20], center=true);
}""",
}

# --- Router ---
def route_prompt(prompt: str) -> str:
    prompt_lower = prompt.lower()
    parametric_keywords = [
        'box', 'cube', 'sphere', 'cylinder', 'cone', 'chair', 'table',
        'house', 'rocket', 'snowman', 'tree', 'car', 'bottle', 'trophy',
        'mushroom', 'cat', 'mm', 'cm', 'height', 'width', 'radius',
        'geometric', 'simple', 'basic', 'robot', 'ring', 'pyramid',
        'hexagon', 'pentagon', 'triangle', 'rectangle', 'square'
    ]
    ai_keywords = [
        'realistic', 'organic', 'animal', 'person', 'face', 'dragon',
        'complex', 'detailed', 'artistic', 'sculpture', 'photo'
    ]
    parametric_score = sum(1 for k in parametric_keywords if k in prompt_lower)
    ai_score = sum(1 for k in ai_keywords if k in prompt_lower)

    # If it's in our shape dictionary, always use parametric
    for key in SHAPES:
        if key in prompt_lower:
            return "parametric"

    return "ai_generator" if ai_score > parametric_score else "parametric"

# --- Mistral SCAD generator (replaces ollama) ---
def mistral_generate_scad(prompt: str) -> str:
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{
            "role": "user",
            "content": (
                "You are an OpenSCAD code generator. "
                "Return ONLY raw OpenSCAD code. No explanation. No markdown. No backticks. "
                "Use only: cube(), sphere(), cylinder(), translate(), rotate(), union(), difference(). "
                "Generate OpenSCAD code for: " + prompt
            )
        }]
    )
    code = response.choices[0].message.content.strip()
    code = re.sub(r'```[a-zA-Z]*', '', code)
    code = code.replace('```', '').strip()
    for keyword in ['union', 'difference', 'cube', 'cylinder', 'sphere', 'translate']:
        if keyword in code:
            code = code[code.find(keyword):]
            break
    return code

# --- find_shape: dictionary first, then Mistral ---
def find_shape(prompt: str) -> str:
    prompt_lower = prompt.lower()
    for key in SHAPES:
        if key in prompt_lower:
            return SHAPES[key]
    # Unknown shape — use Mistral instead of ollama
    return mistral_generate_scad(prompt)

# --- Render with xvfb ---
def render(scad_code, scad_path, png_path, stl_path):
    os.makedirs(os.path.dirname(scad_path), exist_ok=True)
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    with open(scad_path, "w") as f:
        f.write(scad_code)
    subprocess.run(
        ["xvfb-run", "-a", "openscad", "--imgsize=800,600", "--autocenter", "--viewall",
         "-o", png_path, scad_path],
        capture_output=True, timeout=30
    )
    subprocess.run(
        ["xvfb-run", "-a", "openscad", "-o", stl_path, scad_path],
        capture_output=True, timeout=30
    )

# --- Endpoints ---

@app.get("/")
async def root():
    return {"message": "3D Model Generator API Running!"}

@app.post("/generate")
async def generate(request: PromptRequest):
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    scad_path = f"/home/shybyjoseph1/3d-model-generator/models/{name}.scad"
    png_path  = f"/home/shybyjoseph1/3d-model-generator/outputs/{name}.png"
    stl_path  = f"/home/shybyjoseph1/3d-model-generator/outputs/{name}.stl"

    path = route_prompt(request.prompt)
    scad_code = find_shape(request.prompt)
    render(scad_code, scad_path, png_path, stl_path)

    if not os.path.exists(png_path):
        return {"error": "Render failed", "scad_code": scad_code, "path": path}

    with open(png_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    return {"scad_code": scad_code, "image": img_base64, "status": "success", "path": path}

@app.post("/refine")
async def refine(request: RefineRequest):
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    scad_path = f"/home/shybyjoseph1/3d-model-generator/models/{name}.scad"
    png_path  = f"/home/shybyjoseph1/3d-model-generator/outputs/{name}.png"
    stl_path  = f"/home/shybyjoseph1/3d-model-generator/outputs/{name}.stl"

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{
            "role": "user",
            "content": (
                f"You are an OpenSCAD code modifier.\n"
                f"CURRENT CODE:\n{request.previous_scad}\n\n"
                f"INSTRUCTION: {request.instruction}\n\n"
                f"RULES:\n"
                f"- Return ONLY modified OpenSCAD code\n"
                f"- NO explanation, NO markdown, NO backticks\n"
                f"- If bigger/larger: multiply all numbers by 1.5\n"
                f"- If smaller: multiply all numbers by 0.7\n"
                f"- If taller: increase h values by 1.5x\n\n"
                f"MODIFIED CODE:"
            )
        }]
    )
    code = response.choices[0].message.content.strip()
    code = re.sub(r'```[a-zA-Z]*', '', code)
    code = code.replace('```', '').strip()
    for keyword in ['union', 'difference', 'cube', 'cylinder', 'sphere', 'translate']:
        if keyword in code:
            code = code[code.find(keyword):]
            break

    # Fallback if Mistral returns empty
    if not code.strip():
        prev = request.previous_scad
        instruction_lower = request.instruction.lower()
        if any(w in instruction_lower for w in ['bigger', 'larger', 'large']):
            code = re.sub(r'(\d+\.?\d*)', lambda m: str(round(float(m.group())*1.5, 1)), prev)
        elif any(w in instruction_lower for w in ['smaller', 'tiny', 'small']):
            code = re.sub(r'(\d+\.?\d*)', lambda m: str(round(float(m.group())*0.7, 1)), prev)
        elif any(w in instruction_lower for w in ['taller', 'tall']):
            code = re.sub(r'h=(\d+\.?\d*)', lambda m: f"h={round(float(m.group(1))*1.5, 1)}", prev)
        else:
            code = prev

    render(code, scad_path, png_path, stl_path)

    if not os.path.exists(png_path):
        return {"error": "Render failed", "scad_code": code}

    with open(png_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode()

    return {"scad_code": code, "image": img_base64, "status": "success"}

@app.post("/route")
async def route(request: PromptRequest):
    path = route_prompt(request.prompt)
    return {"prompt": request.prompt, "path": path}

@app.get("/download/stl")
async def download_stl():
    stl_files = glob.glob("/home/shybyjoseph1/3d-model-generator/outputs/*.stl")
    if not stl_files:
        return {"error": "No STL files found"}
    latest_stl = max(stl_files, key=os.path.getctime)
    return FileResponse(latest_stl, media_type="application/octet-stream", filename="model.stl")

@app.get("/export/{filename}")
async def export(filename: str):
    stl_path = f"/home/shybyjoseph1/3d-model-generator/outputs/{filename}.stl"
    if os.path.exists(stl_path):
        return {"stl_path": stl_path, "status": "success"}
    return {"error": "File not found"}
