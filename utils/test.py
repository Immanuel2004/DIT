
from fpdf import FPDF
import os

pdf = FPDF()
pdf.add_page()

font_path = os.path.abspath("utils/assets/fonts/DejaVuSans.ttf")
print("Font Path:", font_path)

pdf.add_font("DejaVu", "", font_path, uni=True)
pdf.set_font("DejaVu", size=12)

pdf.cell(0, 10, "Hello from FPDF with DejaVuSans!", ln=True)

output_path = "sample_output.pdf"
pdf.output(output_path)
