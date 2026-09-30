from diffusers import StableDiffusionPipeline
import torch

MODEL_ID = "runwayml/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID
)

if torch.cuda.is_available():
    pipe = pipe.to("cuda")


def generate_image(prompt):
    image = pipe(prompt).images[0]
    return image