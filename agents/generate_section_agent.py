from langgraph.constants import Send
import os
from helpers import get_chatgpt, get_settings
from helpers.utils import read_structured_data, load_image
from models.formatted_responses import IfChartDecision
from models.states import OverallState, SectionState
from enums.prompts import PromptsEnums
from langchain_experimental.utilities import PythonREPL
from langchain_core.messages import HumanMessage
app_settings = get_settings()


def continue_to_seciton_generation(state: OverallState):
    print("Continuing to section generation")
    return [
        Send(
            "section_subgraph",
            SectionState(
                section_title=section_title,
                sections_titles=state.sections_titles,
                input_data_file_path=state.input_data_file_path,
                user_input=state.user_input,
                debug_folder=state.debug_folder,
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
    prompt = PromptsEnums.GRAPH_OR_NO_GRAPH_PROMPT.value.format(
        user_input = state.user_input,
        section_title=state.section_title,
        df_columns=df.columns.to_list(),
        df_head=df.head(),
        input_data_file_path=state.input_data_file_path,
    )
    
    chatgpt = get_chatgpt()
    output = chatgpt.with_structured_output(IfChartDecision, include_raw=True).invoke(
        input=prompt
    )
    parsed: IfChartDecision = output["parsed"]
    return {"section_chart_type": parsed.chart_type,
            "sections_chart_types": [parsed.chart_type]}


def generate_text_only_section_agent(state: SectionState):    
    prompt = PromptsEnums.TEXT_ONLY_SECTION_PROMPT.value.format(
        user_input=state.user_input,
        section_title=state.section_title,
        sections_titles=state.sections_titles,
    )

    chatgpt = get_chatgpt()
    reply = chatgpt.invoke(input=prompt)
    section_content = reply.content
    
    return {
        "section_content": section_content,
        "sections_content": [section_content],
    }


def generate_chart_section_agent(state: SectionState):
    plot_image_path = os.path.join(state.debug_folder, f"{state.section_title} chart.png")
    
    df = read_structured_data(state.input_data_file_path)
    plotly_code_prompt = PromptsEnums.PLOTLY_CODE_PROMPT.value.format(
        section_title=state.section_title,
        df_head=df.head(),
        df_columns=df.columns.to_list(),
        input_file_path=state.input_data_file_path,
        output_plot_path = plot_image_path,
    )
    
    chatgpt = get_chatgpt()
    reply = chatgpt.invoke(input=plotly_code_prompt)
    code = reply.content
    
    pythonREPL = PythonREPL()
    code = pythonREPL.sanitize_input(code)
    plot_code_path = os.path.join(state.debug_folder, f"{state.section_title} chart.py")
    if app_settings.OUTPUT_DEBUG:
        with open(plot_code_path, "w") as f:
            f.write(code)
    
    pythonREPL.run(code)
    if not os.path.exists(plot_image_path):
        raise Exception("Plot image not saved in the expected location: "+plot_image_path)
    
    section_content_prompt = PromptsEnums.CHART_SECTION_PROMPT.value.format(
        section_title=state.section_title,
        sections_titles=state.sections_titles,
        plot_image_path=plot_image_path,
        user_input=state.user_input,
    )
    encoded_chart_image = load_image(plot_image_path)
    
    prompt = HumanMessage(
        content=[
            {"type": "text", "text": section_content_prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_chart_image}"},
            },
        ],
    )
    
    reply = chatgpt.invoke([prompt])
    
    section_content = reply.content
    
    image_path = f"images/{state.section_title}.png"
    return {
        "section_image": image_path,
        "section_content": section_content,
        "sections_content": [section_content],
        "sections_images": [image_path],
    }
