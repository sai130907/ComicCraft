from pathlib import Path
from typing import List

from fpdf import FPDF

from .config import settings
from .schemas import ComicPanel


class PDFService:
    """Creates PDF exports for generated comics."""

    def __init__(self):
        self.output_dir = Path(settings.EXPORT_DIR)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_pdf(
        self,
        title: str,
        panels: List[ComicPanel],
        panel_image_paths: List[str],
    ) -> str:

        safe_title = self._safe_filename(title)

        pdf_filename = f"{safe_title}.pdf"
        pdf_path = self.output_dir / pdf_filename

        pdf = FPDF(
            orientation="P",
            unit="mm",
            format="A4",
        )

        pdf.set_auto_page_break(
            auto=True,
            margin=15,
        )

        # Cover page
        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            26,
        )

        pdf.cell(
            0,
            20,
            title,
            align="C",
        )

        pdf.ln(20)

        pdf.set_font(
            "Helvetica",
            "",
            13,
        )

        pdf.multi_cell(
            0,
            8,
            "Generated with ComicCraft",
            align="C",
        )

        # Comic pages
        for index, panel in enumerate(panels):

            pdf.add_page()

            pdf.set_font(
                "Helvetica",
                "B",
                18,
            )

            pdf.cell(
                0,
                12,
                f"Panel {panel.panel_number}",
                align="C",
            )

            pdf.ln(15)

            if index < len(panel_image_paths):

                image_path = self._convert_to_local_path(
                    panel_image_paths[index]
                )

                if image_path.exists():

                    pdf.image(
                        str(image_path),
                        x=15,
                        y=35,
                        w=180,
                    )

            pdf.ln(145)

            # Dialogue
            pdf.set_font(
                "Helvetica",
                "B",
                12,
            )

            pdf.cell(
                0,
                8,
                "Dialogue:",
            )

            pdf.ln(8)

            pdf.set_font(
                "Helvetica",
                "",
                11,
            )

            pdf.multi_cell(
                0,
                7,
                self._clean_text(panel.dialogue),
            )

            # Narration
            if panel.narration:

                pdf.ln(5)

                pdf.set_font(
                    "Helvetica",
                    "B",
                    12,
                )

                pdf.cell(
                    0,
                    8,
                    "Narration:",
                )

                pdf.ln(8)

                pdf.set_font(
                    "Helvetica",
                    "",
                    11,
                )

                pdf.multi_cell(
                    0,
                    7,
                    self._clean_text(panel.narration),
                )

        pdf.output(str(pdf_path))

        return f"/static/exports/{pdf_filename}"

    @staticmethod
    def _safe_filename(filename: str) -> str:

        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            "_-"
        )

        cleaned = "".join(
            character
            if character in allowed
            else "_"
            for character in filename
        )

        cleaned = cleaned.strip("_")

        return cleaned[:80] or "comic"

    @staticmethod
    def _clean_text(text: str) -> str:

        return (
            text
            .replace("–", "-")
            .replace("—", "-")
            .replace("’", "'")
            .replace("“", '"')
            .replace("”", '"')
            .replace("…", "...")
        )

    @staticmethod
    def _convert_to_local_path(
        url_path: str,
    ) -> Path:

        clean_path = url_path.lstrip("/")

        return Path(clean_path)


pdf_service = PDFService()