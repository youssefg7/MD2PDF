import operator
from typing import Annotated, Optional

from pandas import DataFrame
from pydantic import BaseModel, ConfigDict


class OverallState(BaseModel):
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


class SectionState(BaseModel):
    input_data_file_path: str
    user_input: str
    section_title: str
    section_content: Optional[str] = None
    section_chart_type: Optional[str] = None
    section_image: Optional[str] = None
    sections_titles: Annotated[list[str], operator.add]