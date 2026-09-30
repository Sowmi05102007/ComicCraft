from dotenv import load_dotenv
load_dotenv()

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from google import genai

from app.exporters import save_pdf


# Project folder path
BASE_DIR = Path(__file__).resolve().parent.parent


# FastAPI app
app = FastAPI()


# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# Gemini client
client = genai.Client()


# Request model
class StoryRequest(BaseModel):
    idea: str


# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Generate comic story
@app.post("/generate")
def generate(request: StoryRequest):

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"""
Create a short 5-panel comic story based on this idea:

{request.idea}

Give each panel:
Panel number
Scene description
Dialogue
"""
    )

    return {
        "reply": response.text
    }


# Export comic as PDF
@app.post("/export")
def export_comic(request: StoryRequest):

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"""
Create a short 5-panel comic story based on this idea:

{request.idea}

Give each panel:
Panel number
Scene description
Dialogue
"""
    )

    filename = save_pdf(response.text)

    return {
        "message": "PDF created successfully",
        "filename": filename
    }