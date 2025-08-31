import os

def register_custom_fonts(pdf):
    font_path = os.path.join("utils", "assets", "fonts", "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.set_font("DejaVu", "", 12)
