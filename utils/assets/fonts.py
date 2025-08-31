from fpdf import FPDF

def register_custom_fonts(pdf: FPDF):
    pdf.add_font("DejaVu", "", "utils/assets/fonts/DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "utils/assets/fonts/DejaVuSans-Bold.ttf", uni=True)
    pdf.add_font("DejaVu", "I", "utils/assets/fonts/DejaVuSans-Oblique.ttf", uni=True)
    # pdf.add_font("DejaVu", "BI", "utils/assets/fonts/DejaVuSans-BoldOblique.ttf", uni=True)
