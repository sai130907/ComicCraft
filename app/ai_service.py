import json
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
        """
        Generate five comic panels from the user's story.

        If MOCK_MODE is enabled, sample panels are returned.
        This allows the application to be tested without an API key.
        """

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

The JSON must have this structure:

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
- image_prompt should describe the visual scene clearly.
- Keep the same main character throughout all panels.
- Do not include markdown.
- Do not include ```json.
"""

        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_FLASH_MODEL,
                contents=prompt,
            )

            response_text = response.text.strip()

            # Remove accidental markdown fences if the model adds them.
            if response_text.startswith("```"):
                response_text = response_text.replace("```json", "")
                response_text = response_text.replace("```", "")
                response_text = response_text.strip()

            data = json.loads(response_text)

            panels = data.get("panels", [])

            if len(panels) != settings.PANEL_COUNT:
                raise ValueError(
                    "AI did not return exactly 5 comic panels."
                )

            return [
                ComicPanel(**panel)
                for panel in panels
            ]

        except Exception as exc:
            print(f"AI generation error: {exc}")

            # Fall back to mock panels instead of crashing the application.
            return self._generate_mock_panels(
                story=story,
                character=character,
                setting=setting,
                tone=tone,
                art_style=art_style,
            )

    def _generate_mock_panels(
        self,
        story: str,
        character: str,
        setting: str,
        tone: str,
        art_style: str,
    ) -> List[ComicPanel]:
        """Generate sample panels for testing."""

        short_story = story[:150]

        return [
            ComicPanel(
                panel_number=1,
                scene_description=(
                    f"{character} arrives at {setting} "
                    "and notices that something unusual is happening."
                ),
                dialogue="Something feels different today...",
                narration=(
                    f"The adventure begins with this idea: {short_story}"
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
                    f"{character} investigates the strange situation "
                    "and discovers an unexpected clue."
                ),
                dialogue="Okay... this definitely wasn't here before!",
                narration="The mystery becomes even more interesting.",
                image_prompt=(
                    f"{art_style}, comic book panel, "
                    f"{character} investigating a mysterious clue in "
                    f"{setting}, expressive face"
                ),
            ),
            ComicPanel(
                panel_number=3,
                scene_description=(
                    f"{character} follows the clue and encounters "
                    "a surprising obstacle."
                ),
                dialogue="Wait! How am I supposed to get past this?",
                narration="The challenge suddenly becomes serious.",
                image_prompt=(
                    f"{art_style}, comic book panel, "
                    f"{character} facing an unexpected obstacle in "
                    f"{setting}, dynamic action scene"
                ),
            ),
            ComicPanel(
                panel_number=4,
                scene_description=(
                    f"{character} uses creativity and courage to solve "
                    "the problem."
                ),
                dialogue="I've got an idea!",
                narration="A clever solution changes everything.",
                image_prompt=(
                    f"{art_style}, comic book panel, "
                    f"{character} solving the problem in {setting}, "
                    "dramatic lighting, energetic pose"
                ),
            ),
            ComicPanel(
                panel_number=5,
                scene_description=(
                    f"{character} successfully resolves the situation "
                    "and celebrates the unexpected adventure."
                ),
                dialogue="That was definitely a day to remember!",
                narration="The adventure ends with a surprising smile.",
                image_prompt=(
                    f"{art_style}, comic book final panel, "
                    f"{character} celebrating in {setting}, "
                    "happy ending, cinematic comic composition"
                ),
            ),
        ]


ai_service = AIService()