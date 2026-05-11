from mcp.server.fastmcp import FastMCP
import subprocess
import re
from datetime import datetime
import os

mcp = FastMCP("3D Model Generator", port=8001)

@mcp.tool()
def generate_3d_model(prompt: str) -> str:
    """Generate a 3D model from text description using Ollama and OpenSCAD"""
    result = subprocess.run(
        ["ollama", "run", "mistral",
         "You are OpenSCAD code generator. Return ONLY raw OpenSCAD code. No explanation. No markdown. No backticks. Generate OpenSCAD code for: " + prompt],
        capture_output=True, text=True
    )
    code = result.stdout.strip()
    code = re.sub(r'```[a-zA-Z]*', '', code)
    code = code.replace('```', '').strip()
    code = re.sub(r'(\d+)(mm|cm|m|in)', r'\1', code)
    for keyword in ['module','cube','cylinder','sphere','union','difference']:
        if keyword in code:
            code = code[code.find(keyword):]
            break

    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    scad_path = f"/home/sandra/3d_model_generator/models/{name}.scad"
    png_path = f"/home/sandra/3d_model_generator/outputs/{name}.png"
    stl_path = f"/home/sandra/3d_model_generator/outputs/{name}.stl"

    with open(scad_path, "w") as f:
        f.write(code)

    subprocess.run(["openscad","--imgsize=800,600","--autocenter","--viewall","-o",png_path,scad_path])
    subprocess.run(["openscad","-o",stl_path,scad_path])

    if os.path.exists(png_path):
        return f"Success! PNG: {png_path} | STL: {stl_path} | Code: {code}"
    else:
        return f"Error rendering. Code was: {code}"

@mcp.tool()
def list_generated_models() -> str:
    """List all generated 3D models"""
    outputs = os.listdir("/home/sandra/3d_model_generator/outputs/")
    png_files = [f for f in outputs if f.endswith('.png')]
    return f"Generated models: {', '.join(png_files)}"

@mcp.tool()
def get_openscad_libraries() -> str:
    """List available OpenSCAD libraries"""
    libs = os.listdir("/home/sandra/3d_model_generator/models/libraries/")
    return f"Available libraries: {', '.join(libs)}"

if __name__ == "__main__":
    mcp.run(transport="sse")
