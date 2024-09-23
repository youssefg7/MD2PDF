from pydantic import BaseModel, ConfigDict


class GeneratedSections(BaseModel):
    sections_titles: list[str]
