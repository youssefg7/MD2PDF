import re
import pandas as pd

def read_md(file_path: str) -> str:
    if not file_path.endswith(".md"):
        raise ValueError("File is not a markdown file")
    with open(file_path, "r") as file:
        return file.read()


def read_css(file_path: str) -> str:
    if not file_path.endswith(".css"):
        raise ValueError("File is not a css file")
    with open(file_path, "r") as file:
        file = file.read()
        return f"<style>{file}</style>"


def write_html(html: str, file_path: str) -> None:
    with open(file_path, "w") as file:
        file.write(html)


def auto_direction_html(html: str) -> str:
    """
    Add dir="auto" to all html tags that don't already have it

    Args:
        html (str): The html content to add dir="auto" to

    Returns:
        str: The html content with dir="auto" added to all tags that didn't already have it
    """

    return re.sub(r'(<\w+)([^>]*)(?<!dir="auto")(>)', r'\1\2 dir="auto"\3', html)

def read_structured_data(file_path: str) -> pd.DataFrame:
    if not file_path.endswith(".xlsx" or ".csv"):
        raise ValueError("File is not a structured data file (xlsx or csv)")
    
    if file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)
    
    return pd.read_csv(file_path)

