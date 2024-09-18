OUTPUT_DEBUG = True
OUTPUT_DIR = 'output'

options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None
}

html_template = """
<html>
<head>{css_styles}</head>
<body>{html_content}</body>
</html>
"""