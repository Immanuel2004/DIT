# utils/pdf_exporter_2.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
import os
from utils.report_generator import generate_structured_report_sections


def export_structured_pdf(df, insights_by_category, graph_paths, output_path="exports/generated_report.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    section_space = Spacer(1, 12)

    # Generate content sections
    report = generate_structured_report_sections(df)

    def add_heading(text, level=1):
        style = styles[f"Heading{min(level, 3)}"]
        story.append(Paragraph(text, style))
        story.append(section_space)

    def add_paragraph(text):
        story.append(Paragraph(text, styles["Normal"]))
        story.append(section_space)

    add_heading("1. Executive Summary")
    add_paragraph(report["executive_summary"])

    add_heading("2. Introduction")
    for key, value in report["introduction"].items():
        add_heading(key.capitalize(), level=3)
        add_paragraph(value)

    add_heading("3. Data Overview")
    for key, value in report["data_overview"].items():
        add_heading(key.replace("_", " ").capitalize(), level=3)
        add_paragraph(value)

    add_heading("4. Methodology")
    for key, value in report["methodology"].items():
        add_heading(key.capitalize(), level=3)
        add_paragraph(value)

    add_heading("5. Detailed Analysis & Insights")
    for category, insights in insights_by_category.items():
        add_heading(f"5.{list(insights_by_category).index(category) + 1} Category: {category}", level=2)
        for insight in insights:
            add_paragraph(f"- {insight}")
            if any(keyword in insight for keyword in ["[Insert graph here]", "Visual Representation"]):
                graph_file = graph_paths.get(insight)
                if graph_file and os.path.exists(graph_file):
                    story.append(Image(graph_file, width=400, height=250))
                    story.append(section_space)

    add_heading("6. Cross-Domain Insights")
    add_paragraph(report["cross_domain_insights"])

    add_heading("7. Recommendations & Actionable Items")
    table_data = [["Insight", "Recommended Action", "Priority", "Owner/Team", "Timeline"]]
    for rec in report["recommendations"]:
        table_data.append([rec["insight"], rec["action"], rec["priority"], rec["owner"], rec["timeline"]])
    table = Table(table_data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    story.append(table)
    story.append(section_space)

    add_heading("8. Conclusion")
    add_paragraph(report["conclusion"])

    doc.build(story)
    print(f"PDF exported to: {output_path}")