# 3D Model Generator

A web app that converts text prompts into 3D models using OpenSCAD and Mistral AI.

## Team
- **Shyby ** — Backend API (FastAPI, GCP, OpenSCAD)
- **Athulya ** — Frontend (React/Next.js)
- **Sandra ** — Testing (50 prompt test suite)

## Server
- **VM:** model-server, GCP europe-west3-a
- **IP:** 34.179.225.173
- **Port:** 8000
- **OS:** Ubuntu 24.04

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/generate` | Text prompt → OpenSCAD → PNG image |
| POST | `/refine` | Modify an existing model |
| POST | `/route` | Decide parametric vs AI path |
| GET | `/download/stl` | Download latest STL file |
| GET | `/docs` | Swagger UI (interactive docs) |

## Example Usage

### Generate a model
```bash
curl -X POST http://34.179.225.173:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a chair"}'
```

### Refine a model
```bash
curl -X POST http://34.179.225.173:8000/refine \
  -H "Content-Type: application/json" \
  -d '{"previous_scad": "cube([30,20,10]);", "instruction": "make it bigger"}'
```

### Check routing
```bash
curl -X POST http://34.179.225.173:8000/route \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a realistic dragon"}'
```

## How It Works

1. User sends a text prompt to `/generate`
2. Router checks if it matches a known shape (chair, table, car, etc.)
3. **Known shapes** → returns pre-built OpenSCAD code (fast)
4. **Unknown shapes** → sends to Mistral AI to generate OpenSCAD code
5. OpenSCAD renders the code into a PNG image and STL file
6. API returns base64 image + STL download link

## Supported Shapes (parametric)
box, sphere, cylinder, cone, cube, chair, table, house, snowman, rocket,
mushroom, cat, tree, car, bottle, trophy, robot, ring, pyramid,
hexagon, pentagon, triangle, rectangle, square

## Tech Stack
- **Backend:** Python, FastAPI, Uvicorn
- **3D Rendering:** OpenSCAD, xvfb
- **AI:** Mistral API (mistral-small-latest)
- **Cloud:** Google Cloud Platform (e2-medium)
- **Frontend:** React 

## Restart Server
```bash
cd ~/3d-model-generator
source venv/bin/activate
uvicorn scripts.api:app --host 0.0.0.0 --port 8000 &
```

## Environment Variables
Create a `.env` file in the project root:
```
MISTRAL_API_KEY=your_key_here
```
