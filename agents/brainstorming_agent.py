from helpers import get_chatgpt
from helpers.utils import read_structured_data
from models.formatted_responses import GeneratedSections
from models.states import OverallState
from enums.prompts import PromptsEnums

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
    state.sections_titles = parsed.sections_titles
    return state
