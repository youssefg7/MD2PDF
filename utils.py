def read_md(file_path: str) -> str:
    if not file_path.endswith('.md'):
        raise ValueError('File is not a markdown file')
    with open(file_path, 'r') as file:
        return file.read()

def read_css(file_path: str) -> str:
    if not file_path.endswith('.css'):
        raise ValueError('File is not a css file')
    with open(file_path, 'r') as file:
        file = file.read()
        return f'<style>{file}</style>'
    
    
def write_html(html: str, file_path: str) -> None:
    with open(file_path, 'w') as file:
        file.write(html)
    
    
    
