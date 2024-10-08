import os
import time

from langgraph.graph import END, START, StateGraph
import asyncio

from agents import (
    brainstorming_agent,
    collect_sections_agent,
    continue_to_seciton_generation,
    continue_with_chart_generation,
    continue_with_decision,
    decide_section_agent,
    generate_chart_section_agent,
    generate_text_only_section_agent,
    summary_agent,
)
from models.states import OverallState, SectionState, SectionStateOutput

section_builder = StateGraph(state_schema=SectionState, output=SectionStateOutput)
section_builder.add_node("decide_section_agent", decide_section_agent)
section_builder.add_node(
    "generate_text_only_section_agent", generate_text_only_section_agent
)
section_builder.add_node("generate_chart_section_agent", generate_chart_section_agent)
section_builder.add_edge(START, "decide_section_agent")
section_builder.add_conditional_edges(
    "decide_section_agent",
    continue_with_decision,
    ["generate_text_only_section_agent", "generate_chart_section_agent"],
)
section_builder.add_edge("generate_chart_section_agent", END)
# section_builder.add_conditional_edges(
#     "generate_chart_section_agent",
#     continue_with_chart_generation,
#     {
#         "end": END,
#         "reflect": "generate_chart_section_agent"
#     }
# )
section_builder.add_edge("generate_text_only_section_agent", END)

section_graph = section_builder.compile()
# section_graph_image = section_graph.get_graph().draw_mermaid_png()
# with open("section_graph.png", "wb") as f:
#     f.write(section_graph_image)


builder = StateGraph(state_schema=OverallState)

builder.add_node("brainstorming_sections_agent", brainstorming_agent)
builder.add_node("section_subgraph", section_graph)
builder.add_node("summary_agent", summary_agent)
builder.add_node("collect_sections_agent", collect_sections_agent)


builder.add_edge(START, "brainstorming_sections_agent")
builder.add_conditional_edges(
    "brainstorming_sections_agent",
    continue_to_seciton_generation,
    ["section_subgraph"],
)
builder.add_edge("section_subgraph", "summary_agent")
builder.add_edge("summary_agent", "collect_sections_agent")
builder.add_edge("collect_sections_agent", END)


graph = builder.compile()
# graph_image = graph.get_graph().draw_mermaid_png()
# with open("graph.png", "wb") as f:
#     f.write(graph_image)


graph_time = str(time.strftime("%Y-%m-%d-%H-%M-%S"))
debug_folder = os.path.join("output", "debug", graph_time)
os.makedirs(debug_folder, exist_ok=True)

output_folder = os.path.join("output/pdf", graph_time)
os.makedirs(output_folder, exist_ok=True)
output_pdf_path = os.path.join(output_folder, "output.pdf")

input_data_file_path = "input-samples/Sale Data.xlsx"
user_input = "A monthly sales report"

start = time.time()


loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
# loop.run_until_complete(graph.ainvoke(
#     OverallState(
#         input_data_file_path=input_data_file_path,
#         user_input=user_input,
#         output_pdf_path=output_pdf_path,
#         debug_folder=debug_folder,
#     )
# ))
# loop.close()

graph.invoke(
    OverallState(
        input_data_file_path=input_data_file_path,
        user_input=user_input,
        output_pdf_path=output_pdf_path,
        debug_folder=debug_folder,
    )
)
end = time.time()

print(f"Time taken: {end-start} seconds", flush=True)
