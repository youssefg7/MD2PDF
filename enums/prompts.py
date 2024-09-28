from enum import Enum


class PromptsEnums(Enum):
    BRAINSTORMING_PROMPT = """
You are an expert document writer. You have been asked to write a '{user_input}'.
Complete the list of sections that you would include in the report, if the first section title is '1. Executive Summary'

You have the following data available:

Sample data from {input_data_file_path}:
{df_head}

Available columns in the data:
{df_columns}

Instructions:
- Please return a numbered list of sections starting from 2.
- All the titles should be in the format '2. Section Title'.
- Only include main body sections, no conclusion , appendix, references, suggestions, acknowledgments or any other similar sections.
- The list should be at least 3 sections long and no longer than 7 sections.
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
- The markdown must start with a header of level 1 (#) with the section title.
- Always start your response with triple quotes (```) and end it with triple quotes to ensure that the markdown is formatted correctly.
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
# Create the Output Directory, Ensure that the plot image output directory '{output_plot_path}' exists, use the exact given path.
# Read the input data from '{input_file_path}' into a pandas DataFrame.
# Code to generate a clear and informative plot with plotly-express using the data. 
# Don't forget to include a title, labels, and any other necessary configurations for the plot.
# Make sure to use `fig.update_traces(textposition='none')` after creating the plot to remove numbers on the plot.
# Save aggregate data used to generate the plot to '{used_data_path}', use the exact given path.
# Save the plot image to '{output_plot_path}', use the exact given path.
```

Instructions:
- Output 100% syntatically and logically correct Python code ONLY.
- Ensure that the code is ready to be executed.
- Use 'os' library to create directories, save files and join paths.
"""

    CHART_SECTION_PROMPT = """
You are an expert data reports writer, proficient in writing sections with charts for a report.
Your task is to generate a '{section_title}' section for a '{user_input}' report.
Given the data and the chart attached below, please write the '{section_title}' section.

The report includes the following sections:
{sections_titles}

The data used to generate the chart is:
{used_data}


Instructions:
- Please reply directly with a markdown-formatted text of the section that is ready to be inserted into a markdown file for the report.
- Please place the chart image at a suitable location in the section markdown text given that its path is: '{plot_image_path}'
- The markdown must start with a header of level 1 (#) with the section title.
- Always start your response with triple quotes (```) and end it with triple quotes to ensure that the markdown is formatted correctly.
"""

    EXECUTIVE_SUMMARY_PROMPT = """
You are an expert data reports writer, proficient in writing executive summaries for a report.
Your task is to generate an '1. Executive Summary' section for a '{user_input}' report.

The report includes the following sections:
{report_content}

Instructions:
- Please Reply directly with a markdown-formatted text of the executive summary that is ready to be inserted into a markdown file for the report.
- The markdown must start with '# 1. Executive Summary'.
- The section should highlight the key points of the report.
- Always start your response with triple quotes (```) and end it with triple quotes to ensure that the markdown is formatted correctly.

"""
