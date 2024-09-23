from models.states import SectionsState, OutputState

def collect_sections_agent(state: SectionsState):
    print("Collecting sections")
    return OutputState(output_pdf_path="output.pdf")
    