import base64
import os
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
    Add dir="auto" to all html tags that don't already have it to support right-to-left languages, such as Arabic.
    It doesn't add dir="auto" to closing tags, self-closing tags or tags that already have dir="auto".
    
    Args:
        html (str): The html content to add dir="auto" to.

    Returns:
        str: The html content with dir="auto" added to all tags that didn't already have it.
    """

    return re.sub(r'(<\w+)([^>]*)(?<!dir="auto")(?<!/)(>)', r'\1\2 dir="auto"\3', html)


def absolute_path_html_resources(html: str) -> str:
    """
    Replace relative paths in html resources with absolute paths

    Args:
        html (str): The html content to replace relative paths in

    Returns:
        str: The html content with relative paths replaced with absolute paths
    """

    return re.sub(
        r'(src|href)="(?!http)([^"]+)"', rf'\1="{os.path.abspath(".")}/\2"', html
    )


def read_structured_data(file_path: str) -> pd.DataFrame:
    if not file_path.split(".")[-1] in ["xlsx", "csv"]:
        raise ValueError(
            f"File {file_path} is not a structured data file (xlsx or csv)"
        )

    if file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)

    return pd.read_csv(file_path)


def load_image(image_path: str) -> str:
    """Load image from file and encode it as base64."""

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    image_base64 = encode_image(image_path)
    return image_base64


def process_html(html: str) -> str:
    html = auto_direction_html(html)
    html = absolute_path_html_resources(html)
    return html


if __name__ == "__main__":
    # print(read_md("input-samples/sample.md"))
    # print(read_css("assets/styles.css"))
    # write_html("test", "output.html")
    # print(auto_direction_html("<html>"))
    print(absolute_path_html_resources('<html><img src="image.png" /></html>'))
    # print(read_structured_data("input-samples/Sale Data.xlsx"))
    # print(load_image("input-samples/sample.png"))
    # print(process_html("<html>"))
