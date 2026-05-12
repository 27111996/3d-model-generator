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
  translate([0,0,18]) sphere(r=7);
  translate([0,0,28]) sphere(r=5);
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
    "bottle": """union() {
  cylinder(h=30, r=10);
  translate([0,0,30]) cylinder(h=15, r1=10, r2=4);
  translate([0,0,45]) cylinder(h=10, r=4);
}""",
}

def find_shape(prompt: str) -> str:
    prompt_lower = prompt.lower()
    for key in SHAPES:
        if key in prompt_lower:
            return SHAPES[key]
    result = subprocess.run(
        ["ollama", "run", "llama3.2:3b",
         "Generate simple OpenSCAD code using ONLY cube(), sphere(), cylinder(), translate(), union(). NO variables. NO loops. Return ONLY code. For: " + prompt],
        capture_output=True, text=True
    )
    code = result.stdout.strip()
    code = re.sub(r'```[a-zA-Z]*', '', code)
    code = code.replace('```', '').strip()
    for keyword in ['union','difference','cube','cylinder','sphere','translate']:
        if keyword in code:
            code = code[code.find(keyword):]
            break
    return code

@app.post("/generate")
async def generate(request: PromptRequest):
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    scad_path = f"/home/sandra/3d_model_generator/models/{name}.scad"
    png_path = f"/home/sandra/3d_model_generator/outputs/{name}.png"
    stl_path = f"/home/sandra/3d_model_generator/outputs/{name}.stl"
    scad_code = find_shape(request.prompt)
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
