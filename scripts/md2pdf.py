import argparse
import os
import sys

import markdown2
import pdfkit

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from helpers import get_settings
from helpers.utils import process_html, read_css, read_md, write_html

app_settings = get_settings()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert markdown to pdf")
    parser.add_argument("input_md_path", type=str, help="Input markdown file")
    args = parser.parse_args()
    input_md_path = args.input_md_path

    if not os.path.exists(app_settings.OUTPUT_DIR):
        os.makedirs(app_settings.OUTPUT_DIR)
    output_pdf_file = (input_md_path.split("/")[-1]).split(".")[0] + ".pdf"
    output_pdf_path = os.path.join(app_settings.OUTPUT_DIR, output_pdf_file)

    md = read_md(input_md_path)
    html = markdown2.Markdown(extras=["tables", "fenced-code-blocks"]).convert(md)
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
        debug_dir = os.path.join(app_settings.OUTPUT_DIR, "debug")
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
        output_html_file = (input_md_path.split("/")[-1]).replace(".md", ".html")
        output_html_path = os.path.join(debug_dir, output_html_file)
        write_html(formatted_template, output_html_path)
    pdfkit.from_string(
        formatted_template, output_pdf_path, options=app_settings.OPTIONS
    )
    print(f"PDF generated at {output_pdf_path}")
