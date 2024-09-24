from langgraph.constants import Send

from models.states import OverallState, SectionState
from models.formatted_responses import IfChartDecision
from helpers import get_chatgpt
from helpers.utils import read_structured_data

def continue_to_seciton_generation(state: OverallState):
    return [
        Send("decide_section_agent", SectionState(
            section_title=section_title,
            **state.dict()
            ))
        for section_title in state.sections_titles
    ]

def continue_with_decision(state: SectionState) -> str:
    print("Continuing with decision for section", state.section_title, "decision", state.section_chart_type)
    if state.section_chart_type == "no chart needed":
        return "generate_text_only_section"
    else:
        return "generate_chart_section"

def decide_section_agent(state: SectionState):
    df = read_structured_data(state.input_data_file_path)
    prompt = f"""
You are an expert data reports writer, proficient in choosing the right chart type for each section of a report. You are tasked with generating a section for a report titled '{state.section_title}'.
The document includes the following sections:
{state.sections_titles}


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
    state.section_chart_type = parsed.chart_type
    
    return state

def generate_text_only_section_agent(state: SectionState):
    print("Generating section ", state.section_title)
    return state

def generate_chart_section_agent(state: SectionState):
    print("Generating section with chart", state.section_title)
    return state