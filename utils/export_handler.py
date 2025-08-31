# export_handler.py
from utils.report_generator import generate_pdf_report as create_pdf_report, export_to_pptx

def generate_pdf_report(session):
    return create_pdf_report(session)

def generate_pptx_report(session):
    return export_to_pptx(session)
