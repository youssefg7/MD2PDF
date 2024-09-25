from enum import Enum


class PromptsEnums(Enum):
    BRAINSTORMING_PROMPT = """
You are an expert document writer. You have been asked to write a '{user_input}'.
Generate a list of sections that you would include in the report, if you have the following data.

Sample data from {input_data_file_path}:
{df_head}

Available columns in the data:
{df_columns}

Return a numbered list of sections.
"""

    GRAPH_OR_NO_GRAPH_PROMPT = """
You are an expert data reports writer, proficient in choosing the right chart type for each section of a report. You are tasked with generating a section for a report titled '{user_input}'.
The document includes the following sections:

Given that the data includes the following columns:
{df_columns}

Sample data from {input_data_file_path}:
{df_head}

You are now working on the section titled '{section_title}'.
Please choose one chart type (bar chart, line chart, table, pie chart, histogram, timeline, scatter, heatmap, or any other python plotly express chart type) that you think would be needed for {section_title} section, ONLY if needed.
If no graph is needed for this section, return 'no chart needed'.
"""

    TEXT_ONLY_SECTION_PROMPT = """
You are an expert data reports writer, proficient in writing text-only sections for a report. 
You are tasked is to generate a text-only '{section_title}' section for a '{user_input}' report.

This report includes the following sections:
{sections_titles}

Instructions:
- Reply directly with a markdown-formatted text-only section for the section titled '{section_title}'.
- The paragraph should be at least 3 sentences long and no longer than 5 sentences.
- Your response should be a paragraph of markdown-formatted text that is ready to be inserted into a markdown file for the report.
- The markdown must start with a header of level 2 (##) with the section title.
- Always start your response with triple quotes and end it with triple quotes to ensure that the markdown is formatted correctly.
"""

    PLOTLY_CODE_PROMPT = """
You are an intelligent assistant proficient in Python programming, specifically in generating and executing code to plot figures using plotly-express.        
Please write a python script that creates a plot in Python with plotly-express package.
The generated script should include all necessary imports and configurations for plotly-express.

Sample data from {input_file_path}
{df_head}

Available columns in the data:
{df_columns}

Plot should contain: {section_title}

Update the python code below to generate the plot:        

```python
# TODO 
# Import required dependencies.
# Create the Output Directory, Ensure that the plot image output directory '{output_plot_path}' exists.
# Read the input data from '{input_file_path}' into a pandas DataFrame.
# Code to generate a clear and informative plot.
# Save the plot image to '{output_plot_path}'
```

Output 100% syntatically and logically correct Python code ONLY.
"""

    CHART_SECTION_PROMPT = """
You are an expert data reports writer, proficient in writing sections with charts for a report.
Your task is to generate a '{section_title}' section for a '{user_input}' report.

The report includes the following sections:
{sections_titles}

Given the chart attached below, please write the '{section_title}' section.

Instructions:
- Please reply directly with a markdown-formatted text of the section that is ready to be inserted into a markdown file for the report.
- Please place the chart image at a suitable location in the section markdown text given that its path is: '{plot_image_path}'
- The markdown must start with a header of level 2 (##) with the section title.
- Always start your response with triple quotes and end it with triple quotes to ensure that the markdown is formatted correctly.
"""
