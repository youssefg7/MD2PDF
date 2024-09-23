from langgraph.graph import END, START, StateGraph
from models.states import OverallState, InputState, OutputState, SectionsState, SectionState
from agents import brainstorming_agent, generate_section_agent, continue_to_seciton_generation, collect_sections_agent

builder = StateGraph(state_schema=OverallState, input=InputState, output=OutputState)

builder.add_node("brainstorming_sections_agent", brainstorming_agent)
builder.add_node("generate_section_agent", generate_section_agent)
builder.add_node("collect_sections_agent", collect_sections_agent)

builder.add_edge(START, "brainstorming_sections_agent")
builder.add_conditional_edges("brainstorming_sections_agent", continue_to_seciton_generation, ["generate_section_agent"])
builder.add_edge("generate_section_agent", "collect_sections_agent")
builder.add_edge("collect_sections_agent", END)



graph = builder.compile()
graph_image = graph.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(graph_image)

for s in graph.stream(
    OverallState(
        input_data_file_path="input-samples/Sale Data.xlsx",
        user_input="A sales report",
        sections_titles=[],
        sections_content=[],
        sections_images=[],
        output_pdf_path="output.pdf"
    )
):
    print(s)