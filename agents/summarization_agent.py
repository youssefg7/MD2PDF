from enums.prompts import PromptsEnums
from models.states import OverallState
from helpers import get_chatgpt

def summary_agent(state:OverallState):
    prompt = PromptsEnums.EXECUTIVE_SUMMARY_PROMPT.value.format(
        user_input = state.user_input,
        report_content = "\n\n".join(state.sections_content)
    )
    
    chatgpt = get_chatgpt()
    output = chatgpt.invoke(input=prompt)
    summary = output.content.strip('```')
    
    return {
        'exec_summary': summary
    }
    
    
    
    