from fastapi import FastAPI
from mistralai import Mistral
import subprocess

app = FastAPI()

client = Mistral(api_key="ZpCcPjCxGnfvSqMTt6SGqTuIxeBfYBmP")

def generate_scad(prompt):
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{
            "role": "user",
            "content": "You are an OpenSCAD code generator. Return ONLY raw OpenSCAD code. No explanation. No markdown. Generate OpenSCAD code for: " + prompt
        }]
    )
    return response.choices[0].message.content.strip()

@app.get("/")
def root():
    return {"status": "3D model server running"}

@app.post("/generate")
def generate(prompt: str):
    scad_code = generate_scad(prompt)
    with open("model.scad", "w") as f:
        f.write(scad_code)
    subprocess.run(["xvfb-run", "openscad", "-o", "model.png", "model.scad"])
    return {"status": "done", "scad_code": scad_code}
