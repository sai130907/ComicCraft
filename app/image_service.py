import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from .config import settings


load_dotenv()


class ImageService:
    """Generate comic panel artwork using Hugging Face."""

    def __init__(self):
        self.output_dir = Path(settings.PANEL_DIR)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.token = os.getenv("HF_TOKEN")

        self.model = os.getenv(
            "IMAGE_MODEL",
            "black-forest-labs/FLUX.1-schnell",
        )

        if self.token:
            self.client = InferenceClient(
                api_key=self.token
            )
        else:
            self.client = None

    def generate_panel(
        self,
        panel_number: int,
        scene_description: str,
        image_prompt: str,
    ) -> str:
        """
        Generate one AI comic panel.

        Returns the browser-accessible image URL.
        """

        filename = f"panel_{panel_number}.png"

        output_path = (
            self.output_dir / filename
        )

        prompt = self._build_prompt(
            scene_description=scene_description,
            image_prompt=image_prompt,
        )

        if not self.client:
            raise RuntimeError(
                "HF_TOKEN is missing from the .env file."
            )

        try:
            image = self.client.text_to_image(
                prompt=prompt,
                model=self.model,
            )

            image.save(
                str(output_path)
            )

        except Exception as exc:

            raise RuntimeError(
                "Hugging Face image generation failed: "
                f"{exc}"
            ) from exc

        return (
            f"/static/panels/{filename}"
        )

    @staticmethod
    def _build_prompt(
        scene_description: str,
        image_prompt: str,
    ) -> str:
        """
        Build a consistent comic-style image prompt.
        """

        return f"""
Create a high-quality comic book panel.

Visual style:
clean modern comic-book illustration,
strong line art,
expressive characters,
cinematic composition,
clear foreground and background,
vibrant colors,
professional digital illustration.

Scene:
{scene_description}

Detailed visual prompt:
{image_prompt}

Important requirements:
- Create ONE comic panel.
- Do not create a page containing multiple panels.
- Keep the main character visually consistent.
- Make the scene easy to understand.
- Avoid watermarks.
- Avoid random text.
- Avoid distorted faces or extra limbs.
- Use a polished professional comic illustration style.
""".strip()


image_service = ImageService()