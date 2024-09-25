from models.states import OutputState, OverallState


def collect_sections_agent(state: OverallState):
    print("Collecting sections")
    print(state)
    return OutputState(output_pdf_path="output.pdf")
