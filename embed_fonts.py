# from fpdf import FPDF
# from fpdf.enums import XPos, YPos
# import os

# font_dir = "assets/fonts"
# font_files = [
#     ("DejaVu", "", "DejaVuSans.ttf"),
#     ("DejaVu", "B", "DejaVuSans-Bold.ttf"),
#     ("DejaVu", "I", "DejaVuSans-Oblique.ttf")
# ]

# pdf = FPDF()
# pdf.add_page()

# for family, style, font_file in font_files:
#     font_path = os.path.join(font_dir, font_file)
#     pdf.add_font(family, style, font_path)  # Removed `uni=True` (deprecated)
#     print(f"✅ Font registered: {font_file}")

# pdf.set_font("DejaVu", size=12)
# pdf.cell(0, 10, "Fonts embedded and working ✅", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# pdf.output("test_fonts.pdf")


# import zipfile
# import os

# zip_path = "/Users/joshua/Desktop/Immanuel/Internship_/DIT/dejavu-fonts-ttf-2.37.zip"  # Replace with your actual zip file name
# extract_to = "/Users/joshua/Desktop/Immanuel/Internship_/DIT/assets/fonts"  # Folder to extract contents into

# # Create the folder if it doesn't exist
# os.makedirs(extract_to, exist_ok=True)

# # Extract all contents
# with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#     zip_ref.extractall(extract_to)

# print(f"✅ Extracted '{zip_path}' to '{extract_to}/'")


import zipfile
import os

zip_path = "dejavu-fonts-ttf-2.37.zip"
extract_to = "assets/fonts"

# Ensure target dir exists
os.makedirs(extract_to, exist_ok=True)

# Clean extract
try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✅ Successfully extracted to: {extract_to}")
except zipfile.BadZipFile:
    print("❌ ERROR: Not a valid zip file or it is corrupted.")
except Exception as e:
    print(f"❌ ERROR: {e}")
