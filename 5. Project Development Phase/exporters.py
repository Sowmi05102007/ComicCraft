from fpdf import FPDF
from pathlib import Path


def save_pdf(story, filename="comic.pdf"):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, "ComicCraft - AI Comic Story", ln=True)

    pdf.ln(5)

    image_path = Path(__file__).resolve().parent.parent / "static" / "comic_sample.png"

    if image_path.exists():
        pdf.image(str(image_path), x=10, y=30, w=190)

        pdf.ln(115)

    pdf.set_font("Arial", size=12)

    for line in story.split("\n"):
        if line.strip():
            pdf.multi_cell(0, 8, line)
        else:
            pdf.ln(4)

    pdf.output(filename)

    return filename