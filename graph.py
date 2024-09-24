from langgraph.graph import END, START, StateGraph

from agents import (
    brainstorming_agent,
    collect_sections_agent,
    continue_to_seciton_generation,
    generate_text_only_section_agent,
    decide_section_agent,
    generate_chart_section_agent,
    continue_with_decision,
)
from models.states import (
    InputState,
    OutputState,
    OverallState,
)

builder = StateGraph(state_schema=OverallState, input=InputState, output=OutputState)

builder.add_node("brainstorming_sections_agent", brainstorming_agent)
builder.add_node("decide_section_agent", decide_section_agent)
builder.add_node("generate_text_only_section_agent", generate_text_only_section_agent)
builder.add_node("generate_chart_section_agent", generate_chart_section_agent)
builder.add_node("collect_sections_agent", collect_sections_agent)

builder.add_edge(START, "brainstorming_sections_agent")
builder.add_conditional_edges(
    "brainstorming_sections_agent",
    continue_to_seciton_generation,
    ["decide_section_agent"],
)
builder.add_conditional_edges(
    "decide_section_agent",
    continue_with_decision,
    path_map=
    { # map decision to agent
        "generate_chart_section": "generate_chart_section_agent", 
        "generate_text_only_section": "generate_text_only_section_agent",
    },
)

builder.add_edge("generate_chart_section_agent", "collect_sections_agent")
builder.add_edge("generate_text_only_section_agent", "collect_sections_agent")
builder.add_edge("collect_sections_agent", END)


graph = builder.compile()
graph_image = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(graph_image)


# graph.invoke(
#     OverallState(
#         input_data_file_path="input-samples/Sale Data.xlsx",
#         user_input="A sales report",
#         sections_titles=[],
#         sections_content=[],
#         sections_images=[],
#         output_pdf_path="output.pdf",
#     )
# )

for s in graph.stream(
    OverallState(
        input_data_file_path="input-samples/Sale Data.xlsx",
        user_input="A sales report",
        sections_titles=[],
        sections_content=[],
        sections_images=[],
        sections_chart_types = [],
        output_pdf_path="output.pdf",
    )
):
    pass

