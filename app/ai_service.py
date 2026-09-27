import json
import time
from typing import List

from google import genai

from .config import settings
from .schemas import ComicPanel


class AIService:
    """Handles AI-powered comic story and panel generation."""

    def __init__(self):
        self.client = None

        if settings.GEMINI_API_KEY:
            self.client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

    def generate_panels(
        self,
        story: str,
        character: str,
        setting: str,
        tone: str,
        art_style: str,
    ) -> List[ComicPanel]:

        if settings.MOCK_MODE or self.client is None:
            return self._generate_mock_panels(
                story=story,
                character=character,
                setting=setting,
                tone=tone,
                art_style=art_style,
            )

        prompt = f"""
You are an expert comic-book writer.

Create exactly 5 connected comic panels based on the information below.

STORY:
{story}

MAIN CHARACTER:
{character}

SETTING:
{setting}

TONE:
{tone}

ART STYLE:
{art_style}

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "panels": [
        {{
            "panel_number": 1,
            "scene_description": "...",
            "dialogue": "...",
            "narration": "...",
            "image_prompt": "..."
        }}
    ]
}}

Rules:
- Exactly 5 panels.
- panel_number must be 1, 2, 3, 4, 5.
- Each panel must continue the previous panel.
- Keep dialogue short and natural.
- narration may be empty.
- image_prompt should clearly describe the visual scene.
- Keep the same main character throughout all panels.
- Do not include markdown.
- Do not include ```json.
"""

        response = None

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=settings.GEMINI_FLASH_MODEL,
                    contents=prompt,
                )

                break

            except Exception as exc:
                error_text = str(exc)

                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                ):
                    if attempt < 2:
                        wait_time = 5 * (2 ** attempt)

                        print(
                            "Gemini temporarily unavailable. "
                            f"Retrying in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)
                    else:
                        raise

                else:
                    raise

        if response is None:
            raise RuntimeError(
                "Gemini did not return a response."
            )

        response_text = self._clean_json_response(
            response.text
        )

        try:
            data = json.loads(response_text)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Gemini returned invalid JSON."
            ) from exc

        panels = data.get("panels", [])

        if len(panels) != settings.PANEL_COUNT:
            raise ValueError(
                "AI did not return exactly 5 comic panels."
            )

        return [
            ComicPanel(**panel)
            for panel in panels
        ]

    @staticmethod
    def _clean_json_response(response_text: str) -> str:
        """Remove accidental markdown code fences."""

        response_text = response_text.strip()

        if response_text.startswith("```json"):
            response_text = response_text[7:]

        elif response_text.startswith("```"):
            response_text = response_text[3:]

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        return response_text.strip()

    def _generate_mock_panels(
        self,
        story: str,
        character: str,
        setting: str,
        tone: str,
        art_style: str,
    ) -> List[ComicPanel]:

        short_story = story[:150]

        return [
            ComicPanel(
                panel_number=1,
                scene_description=(
                    f"{character} arrives at {setting} "
                    "and notices something unusual."
                ),
                dialogue="Something feels different today...",
                narration=(
                    f"The adventure begins with this idea: "
                    f"{short_story}"
                ),
                image_prompt=(
                    f"{art_style}, comic book panel, "
                    f"{character} standing in {setting}, "
                    "curious expression, cinematic composition"
                ),
            ),
            ComicPanel(
                panel_number=2,
                scene_description=(
                    f"{character} investigates the strange "
                    "situation and discovers an unexpected clue."
                ),
                dialogue=(
                    "Okay... this definitely wasn't here before!"
                ),
                narration=(
                    "The mystery becomes even more interesting."
                ),
                image_prompt=(
                    f"{art_style}, comic book panel, "
                    f"{character} investigating a mysterious "
                    f"clue in {setting}, expressive face"
                ),
            ),
            ComicPanel(
                panel_number=3,
                scene_description=(
                    f"{character} follows the clue and encounters "
                    "a surprising obstacle."
                ),
                dialogue=(
                    "Wait! How am I supposed to get past this?"
                ),
                narration=(
                    "The challenge suddenly becomes serious."
                ),
                image_prompt=(
                    f"{art_style}, comic book panel, "
                    f"{character} facing an unexpected obstacle "
                    f"in {setting}, dynamic action scene"
                ),
            ),
            ComicPanel(
                panel_number=4,
                scene_description=(
                    f"{character} uses creativity and courage "
                    "to solve the problem."
                ),
                dialogue="I've got an idea!",
                narration=(
                    "A clever solution changes everything."
                ),
                image_prompt=(
                    f"{art_style}, comic book panel, "
                    f"{character} solving the problem in {setting}, "
                    "dramatic lighting, energetic pose"
                ),
            ),
            ComicPanel(
                panel_number=5,
                scene_description=(
                    f"{character} successfully resolves the "
                    "situation and celebrates the adventure."
                ),
                dialogue=(
                    "That was definitely a day to remember!"
                ),
                narration=(
                    "The adventure ends with a surprising smile."
                ),
                image_prompt=(
                    f"{art_style}, comic book final panel, "
                    f"{character} celebrating in {setting}, "
                    "happy ending, cinematic comic composition"
                ),
            ),
        ]


ai_service = AIService()