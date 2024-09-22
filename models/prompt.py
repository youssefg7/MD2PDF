class PlotPrompt:

    def __init__(
        self,
        prompt: str,
        df,
        input_file_path: str,
        output_plot_path: str,
        previous_code: str = None,
        previous_error: str = None,
    ):
        self.prompt = prompt
        self.df = df
        self.previous_code = previous_code
        self.previous_error = previous_error
        self.output_plot_path = output_plot_path
        self.input_file_path = input_file_path

    @property
    def value(self):
        v = f"""
You are an intelligent assistant proficient in Python programming, specifically in generating and executing code to plot figures using plotly-express.        
Please write a python script that creates a plot in Python with plotly-express package.
The generated script should include all necessary imports and configurations for plotly-express.

Sample data from {self.input_file_path}
{self.df.head(5)}

Available columns in the data:
{self.df.columns.to_list()}

Plot should contain: {self.prompt}

Update the python code below to generate the plot:        

```python
# TODO 
# Import required dependencies.
# Create the Output Directory, Ensure that the plot image output directory /output/plots/ exists.
# Read the input data from {self.input_file_path} into a pandas DataFrame.
# Code to generate a clear and informative plot.
# Save the plot image to {self.output_plot_path}
```

Output 100% syntatically and logically correct Python code ONLY.
"""

        if self.previous_code is not None and self.previous_error is not None:
            v += f"""
            
            You generated previously below code:
            {self.previous_code}

            It returned below error:
            {self.previous_error}

            Fix it. Do not return the same code again.
            Only return the correct code.
            """
        return v
