import operator
from typing import Annotated, Optional, TypedDict
from types import SimpleNamespace
from pydantic import BaseModel


class OverallState(SimpleNamespace):
    input_data_file_path: str
    user_input: str
    sections_titles: Annotated[list[str], operator.add]
    sections_content: Annotated[list[str], operator.add]
    sections_chart_types: Annotated[list[str], operator.add]
    sections_images: Annotated[list[str], operator.add]
    output_pdf_path: Optional[str] = None


class InputState(BaseModel):
    input_data_file_path: str
    user_input: str


class OutputState(BaseModel):
    output_pdf_path: str


class SectionState(SimpleNamespace):
    input_data_file_path: str
    user_input: str
    section_title: str
    section_content: Optional[str] = None
    section_chart_type: Optional[str] = None
    section_image: Optional[str] = None
    sections_titles: Annotated[list[str], operator.add]
    sections_content: Annotated[list[str], operator.add]
    sections_chart_types: Annotated[list[str], operator.add]
    sections_images: Annotated[list[str], operator.add]

class SectionStateOutput(BaseModel):
    sections_content: Annotated[list[str], operator.add]
    sections_chart_types: Annotated[list[str], operator.add]
    sections_images: Annotated[list[str], operator.add]