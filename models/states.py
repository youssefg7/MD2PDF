import operator
from types import SimpleNamespace
from typing import Annotated, Optional, TypedDict

from pydantic import BaseModel


class OverallState(SimpleNamespace):
    input_data_file_path: str
    user_input: str
    exec_summary: str = None
    sections_titles: Annotated[list[str], operator.add]
    sections_content: Annotated[list[str], operator.add]
    sections_chart_types: Annotated[list[str], operator.add]
    sections_images: Annotated[list[str], operator.add]
    output_pdf_path: str = None
    debug_folder: str = None


class InputState(BaseModel):
    input_data_file_path: str
    user_input: str


class OutputState(BaseModel):
    output_pdf_path: str


class SectionState(SimpleNamespace):
    input_data_file_path: str
    user_input: str
    section_title: str
    section_content: str = None
    section_chart_type: str = None
    section_image: str = None
    sections_titles: Annotated[list[str], operator.add]
    sections_content: Annotated[list[str], operator.add]
    sections_chart_types: Annotated[list[str], operator.add]
    sections_images: Annotated[list[str], operator.add]
    debug_folder: str = None


class SectionStateOutput(BaseModel):
    sections_content: Annotated[list[str], operator.add]
    sections_chart_types: Annotated[list[str], operator.add]
    sections_images: Annotated[list[str], operator.add]
