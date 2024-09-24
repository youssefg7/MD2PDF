from pydantic import BaseModel, ConfigDict


class GeneratedSections(BaseModel):
    sections_titles: list[str]

class IfChartDecision(BaseModel):
    chart_type: str