import os

import markdown2
import pdfkit

from helpers import get_settings
from helpers.utils import process_html, read_css
from models.states import OverallState

app_settings = get_settings()


def collect_sections_agent(state: OverallState):
    markdown = ""
    for section_content, section_title in zip(
        state.sections_content, state.sections_titles
    ):
        markdown += section_content.strip("```") + "\n\n"

    if app_settings.OUTPUT_DEBUG:
        with open(os.path.join(state.debug_folder, "all sections.md"), "w") as file:
            file.write(markdown)

    html = markdown2.Markdown(extras=["tables", "fenced-code-blocks"]).convert(markdown)
    html = process_html(html)
    css_styles = read_css("assets/styles.css")
    html_template = """
<html>
<head>{css_styles}</head>
<body>{html_content}</body>
</html>
"""
    formatted_template = html_template.format(html_content=html, css_styles=css_styles)

    if app_settings.OUTPUT_DEBUG:
        output_html_path = os.path.join(state.debug_folder, "all_sections.html")
        with open(output_html_path, "w") as file:
            file.write(formatted_template)

    pdfkit.from_string(
        formatted_template, state.output_pdf_path, options=app_settings.OPTIONS
    )
