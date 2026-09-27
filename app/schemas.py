from typing import List, Optional

from pydantic import BaseModel, Field


class ComicRequest(BaseModel):
    story: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="The story idea entered by the user.",
    )

    character: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Main character description.",
    )

    setting: str = Field(
        ...,
        min_length=2,
        max_length=300,
        description="Location or environment of the story.",
    )

    tone: str = Field(
        default="funny",
        max_length=50,
        description="Tone of the comic.",
    )

    art_style: str = Field(
        default="comic book",
        max_length=100,
        description="Visual style of the comic.",
    )


class ComicPanel(BaseModel):
    panel_number: int
    scene_description: str
    dialogue: str
    narration: Optional[str] = None
    image_prompt: str


class ComicResponse(BaseModel):
    title: str
    panels: List[ComicPanel]