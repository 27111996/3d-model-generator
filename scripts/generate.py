import subprocess
import re
from datetime import datetime

def generate_scad(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", "mistral",
         "You are OpenSCAD code generator. Return ONLY raw OpenSCAD code. No explanation. No markdown. No backticks. Generate OpenSCAD code for: " + prompt],
        capture_output=True, text=True
    )
    code = result.stdout.strip()
    code = re.sub(r'```[a-zA-Z]*', '', code)
    code = code.replace('```', '').strip()
    for keyword in ['module','cube','cylinder','sphere','union','difference']:
        if keyword in code:
            code = code[code.find(keyword):]
            break
    return code

def render_scad(scad_code: str, name: str):
    scad_path = f"/home/sandra/3d_model_generator/models/{name}.scad"
    png_path = f"/home/sandra/3d_model_generator/outputs/{name}.png"
    stl_path = f"/home/sandra/3d_model_generator/outputs/{name}.stl"
    with open(scad_path, "w") as f:
        f.write(scad_code)
    subprocess.run(["openscad","--imgsize=800,600","--autocenter","--viewall","-o",png_path,scad_path])
    subprocess.run(["openscad","-o",stl_path,scad_path])
    print(f"PNG: {png_path}")
    print(f"STL: {stl_path}")
    return png_path

def main():
    print("LLM-Based 3D Model Generator")
    prompt = input("Describe your 3D object: ")
    name = datetime.now().strftime("%Y%m%d_%H%M%S")
    print("Generating...")
    scad_code = generate_scad(prompt)
    print(f"Code:\n{scad_code}\n")
    render_scad(scad_code, name)
    print("Done!")

if __name__ == "__main__":
    main()
