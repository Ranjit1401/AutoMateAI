"""Generates a real downloadable PDF itinerary using reportlab. Files are
written to backend/generated_files/ and served via
GET /files/{filename} (see app/api/files.py)."""
import uuid
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.tools.base import BaseTool, ToolError

GENERATED_DIR = Path(__file__).resolve().parent.parent.parent / "generated_files"
GENERATED_DIR.mkdir(exist_ok=True)


class PDFGeneratorTool(BaseTool):
    name = "pdf_generator"
    description = "Generates a downloadable PDF itinerary document."

    def execute(self, title: str, sections: list[dict]) -> dict:
        """`sections` is a list of {"heading": str, "lines": list[str]}."""
        if not title or not sections:
            raise ToolError("A title and at least one section are required to generate a PDF.")

        filename = f"{uuid.uuid4().hex}.pdf"
        filepath = GENERATED_DIR / filename

        try:
            styles = getSampleStyleSheet()
            doc = SimpleDocTemplate(str(filepath), pagesize=A4)
            story = [Paragraph(title, styles["Title"]), Spacer(1, 0.5 * cm)]

            for section in sections:
                story.append(Paragraph(section.get("heading", ""), styles["Heading2"]))
                story.append(Spacer(1, 0.2 * cm))
                for line in section.get("lines", []):
                    story.append(Paragraph(line, styles["BodyText"]))
                story.append(Spacer(1, 0.4 * cm))

            doc.build(story)
        except Exception as exc:  # noqa: BLE001
            raise ToolError(f"PDF generation failed: {exc}") from exc

        return {"filename": filename, "download_path": f"/files/{filename}"}
