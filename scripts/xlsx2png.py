import argparse
import os
import sys
import time

import openai
import pandas as pd
from langchain_experimental.utilities import PythonREPL

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from helpers import get_settings
from helpers.utils import auto_direction_html, read_structured_data
from models import PlotPrompt

app_settings = get_settings()
openai_client = openai.OpenAI(
    api_key=app_settings.OPENAI_API_KEY,
)


def process_html(html: str) -> str:
    html = auto_direction_html(html)
    return html


def generate_plotting_code(
    dataframe: pd.DataFrame,
    input_user_prompt: str,
    input_file_path: str,
    output_plot_image_path: str,
    previous_code: str = None,
    previous_error: str = None,
) -> str:
    prompt = PlotPrompt(
        prompt=input_user_prompt,
        df=dataframe,
        input_file_path=input_file_path,
        output_plot_path=output_plot_image_path,
        previous_code=previous_code,
        previous_error=previous_error,
    ).value

    message = {
        "role": "system",
        "content": prompt,
    }

    chat_completion = openai_client.chat.completions.create(
        model=app_settings.LLM,
        temperature=0,
        messages=[message],
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate image from structured data")
    parser.add_argument("input_file_path", type=str, help="Input data file")
    parser.add_argument(
        "input_user_prompt", type=str, help="User prompt for the AI model"
    )
    args = parser.parse_args()
    input_file_path = args.input_file_path
    input_user_prompt = args.input_user_prompt

    # Create output directory if it doesn't exist
    if not os.path.exists(app_settings.OUTPUT_DIR):
        os.makedirs(app_settings.OUTPUT_DIR)

    file_name = input_file_path.split("/")[-1].split(".")[0]
    output_pdf_file = file_name + ".pdf"
    output_pdf_path = os.path.join(app_settings.OUTPUT_DIR, output_pdf_file)

    output_plot_image = file_name + ".png"
    output_plot_image_path = os.path.join(
        app_settings.OUTPUT_DIR, "plots", output_plot_image
    )

    dataframe = read_structured_data(input_file_path)

    last_error = None
    code = None
    while True:
        code = generate_plotting_code(
            dataframe=dataframe,
            input_user_prompt=input_user_prompt,
            input_file_path=input_file_path,
            output_plot_image_path=output_plot_image_path,
            previous_code=code,
            previous_error=last_error,
        )

        pythonREPL = PythonREPL()
        code = pythonREPL.sanitize_input(code)

        if app_settings.OUTPUT_DEBUG:
            debug_dir = os.path.join(app_settings.OUTPUT_DIR, "debug")
            if not os.path.exists(debug_dir):
                os.makedirs(debug_dir)
            with open(
                os.path.join(
                    debug_dir, file_name + time.strftime("%Y%m%d-%H%M%S") + ".py"
                ),
                "w",
            ) as file:
                file.write(code)
        try:
            pythonREPL.run(code)
            print("globals", pythonREPL.globals)
            print("locals", pythonREPL.locals)
            if not os.path.exists(output_plot_image_path):
                raise Exception("Plot image not saved in the expected location.")
            break
        except Exception as e:
            print("Error running code, retrying...")
            last_error = str(e)

    print("\nPlot image saved at: ", output_plot_image_path)
