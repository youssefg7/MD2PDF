from helpers import get_chatgpt
from helpers.utils import read_structured_data
from models.formatted_responses import GeneratedSections
from models.states import OverallState


def brainstorming_agent(state: OverallState):
    print("Brainstorming...")
    df = read_structured_data(state.input_data_file_path)

    prompt = f"""
You are an expert document writer. You have been asked to write a '{state.user_input}'.
Generate a list of sections that you would include in the report, if you have the following data.

Sample data from {state.input_data_file_path}:
{df.head()}

Available columns in the data:
{df.columns.to_list()}

Return a numbered list of sections.
"""

    chatgpt = get_chatgpt()
    output = chatgpt.with_structured_output(GeneratedSections, include_raw=True).invoke(
        input=prompt
    )

    parsed: GeneratedSections = output["parsed"]
    state.sections_titles = parsed.sections_titles
    print("Sections brainstormed:", state.sections_titles)
    return state
