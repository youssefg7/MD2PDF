import argparse
import os
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import shlex

from helpers import get_settings

app_settings = get_settings()

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Convert latex to pdf")
    # parser.add_argument("input_tex_project_path", type=str, help="Input tex project path")
    # args = parser.parse_args()
    # input_tex_project_path = args.input_tex_project_path

    latex_project_folder = "input-samples/Spring24_Graduation_Project_Overleaf_Project/"
    main_tex_file = "main.tex"
    main_tex_file_path = os.path.abspath(
        os.path.join(latex_project_folder, main_tex_file)
    )
    output_dir = "output/tex2html/" + latex_project_folder.split("/")[-2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    command = f'plastex --dir="{output_dir}" "{main_tex_file_path}"'

    proc = subprocess.run(shlex.split(command))
    try:
        print(proc.check_returncode())
        print("Tex to html conversion completed successfully")
    except subprocess.CalledProcessError as e:
        print(e)
        print("Tex to html conversion failed")
