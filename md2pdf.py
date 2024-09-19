import argparse
import os

import markdown2
import pdfkit

from config import OUTPUT_DEBUG, OUTPUT_DIR, html_template, options
from utils import read_css, read_md, write_html, auto_direction_html

def process_html(html: str) -> str:
    html = auto_direction_html(html)
    return html

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert markdown to pdf")
    parser.add_argument("input_md_path", type=str, help="Input markdown file")
    args = parser.parse_args()
    input_md_path = args.input_md_path

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    output_pdf_file = (input_md_path.split("/")[-1]).replace(".md", ".pdf")
    output_pdf_path = os.path.join(OUTPUT_DIR, output_pdf_file)

    md = read_md(input_md_path)
    html = markdown2.Markdown(extras=["tables", "fenced-code-blocks"]).convert(md)
    html = process_html(html)
    
    if OUTPUT_DEBUG:
        output_html_file = (input_md_path.split("/")[-1]).replace(".md", ".html")
        output_html_path = os.path.join(OUTPUT_DIR, output_html_file)
        write_html(html, output_html_path)

    css_styles = read_css("styles.css")
    template = html_template.format(html_content=html, css_styles=css_styles)
    
    pdfkit.from_string(template, output_pdf_path, options=options)
    print(f"PDF generated at {output_pdf_path}")
