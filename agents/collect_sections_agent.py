import asyncio
import os
import time

import markdown2
import pdfkit
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from helpers import get_settings
from helpers.utils import process_html, read_css
from models.states import OverallState

app_settings = get_settings()


def collect_sections_agent(state: OverallState):
    markdown = state.exec_summary + "\n\n"
    body = "\n\n".join(state.sections_content)
    markdown += body

    if app_settings.OUTPUT_DEBUG:
        with open(os.path.join(state.debug_folder, "all sections.md"), "w") as file:
            file.write(markdown)

    html = markdown2.Markdown(extras=["tables", "fenced-code-blocks"]).convert(markdown)
    html = process_html(html)
    toc_md = extract_headings(html)
    toc_html = markdown2.Markdown(extras=["tables", "fenced-code-blocks"]).convert(
        toc_md
    )
    toc_html = process_html(toc_html)
    html = f"{toc_html}\n\n{html}"

    css_styles = read_css("assets/styles.css")
    html_template = """
<html>
<head>{css_styles}</head>
<body class="document_container">{html_content}</body>
</html>
"""
    formatted_template = html_template.format(html_content=html, css_styles=css_styles)

    output_html_path = os.path.join(state.debug_folder, "all_sections.html")
    with open(output_html_path, "w") as file:
        file.write(formatted_template)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        print(os.path.abspath(output_html_path))
        page.goto(f"file://{os.path.abspath(output_html_path)}")
        page.pdf(
            path=state.output_pdf_path,
            format="A4",
            margin={
                "top": "0.75in",
                "right": "0.75in",
                "bottom": "0.75in",
                "left": "0.75in",
            },
            print_background=True,
            scale=1,
        )
        browser.close()


def extract_headings(
    html,
    outline_title="Outline",
    main_heading_title="Main Heading",
    subheading_title="Subheading",
):
    soup = BeautifulSoup(html, "html.parser")

    headings = []
    current_main_heading = ""
    subheadings = []

    for heading in soup.find_all(["h1", "h2"]):
        if heading.name == "h1":
            if current_main_heading:
                print(current_main_heading, subheadings)
                headings.append((current_main_heading, ", ".join(subheadings)))

            current_main_heading = heading.text.strip()
        elif heading.name == "h2":
            print("subheading", heading.text.strip())
            subheadings.append(heading.text.strip())

    if current_main_heading:
        headings.append((current_main_heading, ", ".join(subheadings)))

    table_markdown = f"# {outline_title}\n\n| {main_heading_title}   | {subheading_title}       |\n|----------------|------------------|\n"
    for main_heading, subheading in headings:
        table_markdown += f"| {main_heading} | {subheading} |\n"

    return table_markdown
