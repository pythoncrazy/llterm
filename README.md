# Use an LLM in your terminal!
- This allows you to generate commands, which you can then run easily

## Installation:
- Make sure that you are on a Unix-like computer, such as MacOS or Linux-based computer (such as Ubuntu/Arch, where this code was tested)
- Either use the provided requirements.txt, or use the environment.yml to actually generate the environment

### Conda-specific (using environmnent.yml):
- `conda env create -f environment.yml`, creating the conda environment
### Pip-specific (using requirements.txt):
- `pip install -r requirements.txt`, assuming you are in the same directory as the requirements.txt file

### General Instructions:
- Find which python environment/interpreter you would like to use. This will depend on conda/pip specifics, but it should be pretty easy to find (using `which python`)
- Then, use this as a shebang, once you found the path to the python interpreter (mine is given in the main.py file), place this at the top of the `main.py` file
- Get your NVIDIA NIM token by using the following guide: [LangChain NVIDIA Setup Guide](https://python.langchain.com/v0.2/docs/integrations/chat/nvidia_ai_endpoints/#setup), and place this in the .env file (a sample .env has been given with .env.example)