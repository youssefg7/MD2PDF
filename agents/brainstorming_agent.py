from enums.prompts import PromptsEnums
from helpers import get_chatgpt
from helpers.utils import read_structured_data
from models.formatted_responses import GeneratedSections
from models.states import OverallState


def brainstorming_agent(state: OverallState):
    print("Brainstorming sections...")
    df = read_structured_data(state.input_data_file_path)

    prompt = PromptsEnums.BRAINSTORMING_PROMPT.value.format(
        user_input=state.user_input,
        input_data_file_path=state.input_data_file_path,
        df_head=df.head(),
        df_columns=df.columns.to_list(),
    )

    chatgpt = get_chatgpt()
    output = chatgpt.with_structured_output(GeneratedSections, include_raw=True).invoke(
        input=prompt
    )

    parsed: GeneratedSections = output["parsed"]
    section_titles = parsed.sections_titles

    print("Brainstormed sections:", section_titles)
    if section_titles[0].startswith("1.") and section_titles[1].startswith("2."):
        print("Removed the first section title", section_titles[0])
        section_titles = section_titles[1:]

    return {
        "sections_titles": section_titles,
    }
