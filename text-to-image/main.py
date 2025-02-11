from fastapi import FastAPI, HTTPException
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
import torch
from diffusers import StableDiffusionPipeline

class PromptRequest(BaseModel):
    prompt: str

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(title="Text-to-image API", middleware=middleware)

model_id = "sd-legacy/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

@app.post("/generate")
async def generate_image(request: PromptRequest):
    try:
        image = pipe(request.prompt).images[0]
        output_path = "output.png"
        image.save(output_path)

        return FileResponse(path=output_path, media_type="image/png", filename="output.png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to text-to-image API!"}