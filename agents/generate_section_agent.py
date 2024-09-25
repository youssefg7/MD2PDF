from langgraph.constants import Send

from helpers import get_chatgpt
from helpers.utils import read_structured_data
from models.formatted_responses import IfChartDecision
from models.states import OverallState, SectionState


def continue_to_seciton_generation(state: OverallState):
    print("Continuing to section generation")
    return [
        Send(
            "section_subgraph",
            SectionState(
                section_title=section_title,
                input_data_file_path=state.input_data_file_path,
                user_input=state.user_input,
            ),
        )
        for section_title in state.sections_titles
    ]


def continue_with_decision(state: SectionState):

    if state.section_chart_type == "no chart needed":
        return Send("generate_text_only_section_agent", state)
    else:
        return Send("generate_chart_section_agent", state)


def decide_section_agent(state: SectionState):
    df = read_structured_data(state.input_data_file_path)
    prompt = f"""
You are an expert data reports writer, proficient in choosing the right chart type for each section of a report. You are tasked with generating a section for a report titled '{state.section_title}'.
The document includes the following sections:

Given that the data includes the following columns:
{df.columns.to_list()}

Sample data from {state.input_data_file_path}:
{df.head()}

You are now working on the section titled '{state.section_title}'.
Please choose one chart type (bar chart, line chart, table, pie chart, histogram, timeline, scatter, heatmap, or any other python plotly express chart type) that you think would be needed for {state.section_title} section, ONLY if needed.
If no graph is needed for this section, return 'no chart needed'.
"""

    chatgpt = get_chatgpt()
    output = chatgpt.with_structured_output(IfChartDecision, include_raw=True).invoke(
        input=prompt
    )
    parsed: IfChartDecision = output["parsed"]
    return {"section_chart_type": parsed.chart_type}


def generate_text_only_section_agent(state: SectionState):
    print("Generating section ", state.section_title)
    return {
        "section_content": state.section_content,
        "sections_titles": [state.section_title],
        "sections_content": [state.section_title],
    }


def generate_chart_section_agent(state: SectionState):
    print("Generating section with chart", state.section_title)
    return {
        "section_image": state.section_title,
        "section_content": state.section_title,
        "sections_titles": [state.section_title],
        "sections_content": [state.section_title],
    }
