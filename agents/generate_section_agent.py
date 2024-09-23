from langgraph.constants import Send

from models.states import OverallState, SectionState


def continue_to_seciton_generation(state: OverallState):
    print("Generating sections fork")
    return [
        Send("generate_section_agent", SectionState(section_title=section_title))
        for section_title in state.sections_titles
    ]


def generate_section_agent(state: SectionState):
    print("Generating section ", state.section_title)
    return SectionState(section_title=state.section_title)
