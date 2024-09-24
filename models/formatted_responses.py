from pydantic import BaseModel


class GeneratedSections(BaseModel):
    sections_titles: list[str]


class IfChartDecision(BaseModel):
    chart_type: str
