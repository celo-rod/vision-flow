import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from diffusers.utils import export_to_gif
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

step = 4 
repo = "ByteDance/AnimateDiff-Lightning"
ckpt = f"animatediff_lightning_{step}step_diffusers.safetensors"
base = "emilianJR/epiCRealism"

adapter = MotionAdapter().to(device, dtype)
adapter_state = load_file(hf_hub_download(repo, ckpt), device=device)
adapter.load_state_dict(adapter_state)

pipe = AnimateDiffPipeline.from_pretrained(
    base,
    motion_adapter=adapter,
    torch_dtype=dtype,
).to(device)

pipe.scheduler = EulerDiscreteScheduler.from_config(
    pipe.scheduler.config,
    timestep_spacing="trailing",
    beta_schedule="linear"
)

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(title="Text-to-gif API", middleware=middleware)

class AnimationRequest(BaseModel):
    prompt: str
    guidance_scale: float = 1.0
    num_inference_steps: int = step

@app.post("/generate")
async def generate_animation(request: AnimationRequest):
    try:
        output = pipe(
            prompt=request.prompt,
            guidance_scale=request.guidance_scale,
            num_inference_steps=request.num_inference_steps
        )
        gif_path = "animation.gif"
        export_to_gif(output.frames[0], gif_path)
        
        return FileResponse(
            path=gif_path,
            media_type="image/gif",
            filename="animation.gif"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to text-to-gif API!"}