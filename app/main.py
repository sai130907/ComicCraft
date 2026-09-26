from pathlib import Path
from typing import Any

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .ai_service import ai_service
from .config import settings
from .image_service import image_service
from .pdf_service import pdf_service
from .schemas import ComicRequest


# ---------------------------------------------------------
# Create required directories
# ---------------------------------------------------------

Path(settings.STATIC_DIR).mkdir(
    parents=True,
    exist_ok=True,
)

Path(settings.TEMPLATE_DIR).mkdir(
    parents=True,
    exist_ok=True,
)

Path(settings.PANEL_DIR).mkdir(
    parents=True,
    exist_ok=True,
)

Path(settings.EXPORT_DIR).mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered comic story creator.",
)


# ---------------------------------------------------------
# Static files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=settings.STATIC_DIR),
    name="static",
)


# ---------------------------------------------------------
# Jinja2 templates
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=settings.TEMPLATE_DIR,
)


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def generate_comic_data(
    comic_request: ComicRequest,
) -> dict[str, Any]:
    """
    Complete ComicCraft generation workflow:

    1. Generate 5 comic panels with AI.
    2. Generate an image for each panel.
    3. Build the final layout.
    4. Export the comic to PDF.
    """

    panels = ai_service.generate_panels(
        story=comic_request.story,
        character=comic_request.character,
        setting=comic_request.setting,
        tone=comic_request.tone,
        art_style=comic_request.art_style,
    )

    panel_image_paths = []

    for panel in panels:
        image_path = image_service.generate_panel(
            panel_number=panel.panel_number,
            scene_description=panel.scene_description,
            image_prompt=panel.image_prompt,
        )

        panel_image_paths.append(image_path)

    layout = []

    for panel, image_path in zip(
        panels,
        panel_image_paths,
    ):
        layout.append(
            {
                "panel_number": panel.panel_number,
                "title": f"Panel {panel.panel_number}",
                "image": image_path,
                "scene_description": panel.scene_description,
                "dialogue": panel.dialogue,
                "narration": panel.narration,
                "image_prompt": panel.image_prompt,
            }
        )

    title = "ComicCraft Comic"

    pdf_path = pdf_service.create_pdf(
        title=title,
        panels=panels,
        panel_image_paths=panel_image_paths,
    )

    return {
        "title": title,
        "panels": panels,
        "layout": layout,
        "pdf_path": pdf_path,
    }


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    """
    Display the ComicCraft homepage.
    """

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.APP_NAME,
        },
    )


# ---------------------------------------------------------
# Generate comic from HTML form
# ---------------------------------------------------------

@app.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate_comic(
    request: Request,
    story: str = Form(...),
    character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form("funny"),
    art_style: str = Form("comic book"),
):
    """
    Receive the HTML form and generate a complete comic.
    """

    try:
        comic_request = ComicRequest(
            story=story,
            character=character,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        result = generate_comic_data(
            comic_request,
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "title": result["title"],
                "layout": result["layout"],
                "pdf_path": result["pdf_path"],
            },
        )

    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "app_name": settings.APP_NAME,
                "error": str(exc),
            },
            status_code=500,
        )


# ---------------------------------------------------------
# Generate comic from JSON API
# ---------------------------------------------------------

@app.post(
    "/generate-comic/json",
)
async def generate_comic_json(
    comic_request: ComicRequest,
):
    """
    Generate a comic through a JSON API request.
    """

    try:
        result = generate_comic_data(
            comic_request,
        )

        return JSONResponse(
            content={
                "success": True,
                "title": result["title"],
                "panels": [
                    panel.model_dump()
                    for panel in result["panels"]
                ],
                "layout": result["layout"],
                "pdf_path": result["pdf_path"],
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# Test image generation
# ---------------------------------------------------------

@app.get(
    "/test-image",
    response_class=HTMLResponse,
)
async def test_image(
    request: Request,
    prompt: str = "A funny student discovering a robot in a college laboratory",
):
    """
    Developer utility for testing panel image generation.
    """

    try:
        image_path = image_service.generate_panel(
            panel_number=99,
            scene_description=prompt,
            image_prompt=prompt,
        )

        return HTMLResponse(
            content=f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ComicCraft Image Test</title>
            </head>

            <body>
                <h1>Image Generation Test</h1>

                <p>
                    Prompt:
                    {prompt}
                </p>

                <img
                    src="{image_path}"
                    style="max-width:800px;"
                >

                <br><br>

                <a href="/">
                    Back to ComicCraft
                </a>
            </body>
            </html>
            """
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# Export success page
# ---------------------------------------------------------

@app.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
    pdf_path: str = "",
):
    """
    Display a PDF export confirmation page.
    """

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "pdf_path": pdf_path,
        },
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
async def health():
    """
    Simple endpoint for checking whether the server is running.
    """

    return {
        "status": "ok",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }