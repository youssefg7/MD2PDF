from pydantic import BaseModel, Field


class GeneratedSections(BaseModel):
    sections_titles: list[str] = Field(description="List of numbered main section titles")


class IfChartDecision(BaseModel):
    chart_type: str = Field(description="Type of plotly express chart to generate")
