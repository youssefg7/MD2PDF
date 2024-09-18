import pdfkit
import markdown2
from utils import read_md, read_css, write_html
import os
from config import html_template, options, OUTPUT_DIR, OUTPUT_DEBUG
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert markdown to pdf')
    parser.add_argument('input_md_path', type=str, help='Input markdown file')
    args = parser.parse_args()
    input_md_path = args.input_md_path

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    output_pdf_file = (input_md_path.split('/')[-1]).replace('.md', '.pdf')
    output_pdf_path = os.path.join(OUTPUT_DIR, output_pdf_file)

    md = read_md(input_md_path)
    html = markdown2.Markdown(
        extras=["tables", "fenced-code-blocks"]).convert(md)

    if OUTPUT_DEBUG:
        output_html_file = (input_md_path.split('/')[-1]).replace('.md', '.html')
        output_html_path = os.path.join(OUTPUT_DIR, output_html_file)
        write_html(html, output_html_path)

    css_styles = read_css('styles.css')
    template = html_template.format(html_content=html, css_styles=css_styles)

    pdfkit.from_string(template, output_pdf_path, options=options)
    print(f'PDF generated at {output_pdf_path}')