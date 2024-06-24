#!/home/supersketchy/miniforge-pypy3/envs/llm-term/bin/python
## MAKE SURE TO SET THE CORRECT SHEBANG, otherwise the executable file may not run

# Used for parsing the arguments/the LLM configuration
import os
import argparse
import sys

# Used for the Nice UI
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from enum import Enum
import textwrap

# Used for loading the configuration of the model itself
import json  # used to set the various env variables (such as the api keys)
import getpass  # Get the key if not there

# The LLM that can run in the chat
from llterm.LLM import LLM

# Used for running the generated command
import subprocess


# Used for making the options in the nice UI
class SelectSystemOptions(Enum):
    OPT_GEN_SUGGESTIONS = "Generate new suggestions"
    OPT_DISMISS = "Dismiss"
    OPT_NEW_COMMAND = "Enter a new command"


# Colours used for fancy styling
class Colours:
    WARNING = "\033[93m"
    END = "\033[0m"


# Load all of the configuration itself
try:
    with open(os.path.expanduser(f"~/.config/llterm/config.json")) as f:
        config = json.load(f)
except Exception:  # The file doesn't exist, or the config is wrong
    config = {}

for key, value in config.items():
    os.environ[key] = str(value)

# Taken from: https://python.langchain.com/v0.2/docs/integrations/chat/nvidia_ai_endpoints/
# # del os.environ['NVIDIA_API_KEY']  ## delete key and reset
if os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"):
    api_key = os.environ.get("NVIDIA_API_KEY", "")
else:
    api_key = getpass.getpass("NVAPI Key (starts with nvapi-): ")
    assert api_key.startswith("nvapi-"), f"{api_key[:5]}... is not a valid key"
    os.environ["NVIDIA_API_KEY"] = api_key

if os.environ.get("MODEL") != "":
    model = "google/codegemma-7b"
else:
    model = os.environ.get("MODEL")
print(model)

if os.environ.get("MAX_TOKENS") != "":
    max_tokens = 1024
else:
    max_tokens = os.environ.get("MAX_TOKENS")

if (
    os.environ.get("TEMPERATURE") != ""
    or os.environ.get("TEMPERATURE") > 1
    or os.environ.get("TEMPERATURE") < 0
):
    temperature = 0
else:
    temperature = os.environ.get("TEMPERATURE")

with open(os.path.expanduser("~/.config/llterm/config.json"), "w") as f:
        json.dump({"NVIDIA_API_KEY": api_key, "MODEL": model, "MAX_TOKENS": max_tokens, "TEMPERATURE": temperature}, f)

def main():
    # Create the needed objects used to run the model
    llm = LLM(api_key, model, max_tokens, temperature)
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, nargs="*", default=None)
    args = parser.parse_args()
    prompt = " ".join(sys.argv[1:])

    if prompt:
        while True:
            options = llm.get_commands(prompt)
            options.append(SelectSystemOptions.OPT_GEN_SUGGESTIONS.value)
            options.append(SelectSystemOptions.OPT_NEW_COMMAND.value)
            options.append(SelectSystemOptions.OPT_DISMISS.value)

            # Get the terminal width
            terminal_width = os.get_terminal_size().columns

            # For each option for the name value of the Choice,
            # wrap the text to the terminal width
            choices = [
                Choice(
                    name=textwrap.fill(option, terminal_width, subsequent_indent="  "),
                    value=option,
                )
                for option in options
            ]
            try:
                selection = inquirer.select(
                    message="Select a command:", choices=choices
                ).execute()

                try:
                    if selection == SelectSystemOptions.OPT_DISMISS.value:
                        sys.exit(0)
                    elif selection == SelectSystemOptions.OPT_NEW_COMMAND.value:
                        prompt = input("New command: ")
                        continue
                    elif selection == SelectSystemOptions.OPT_GEN_SUGGESTIONS.value:
                        continue
                    if os.environ.get("SHAI_SKIP_CONFIRM") != "true":
                        user_command = inquirer.text(
                            message="Confirm:", default=selection
                        ).execute()
                    else:
                        user_command = selection

                    # Run the  code directly
                    subprocess.run(user_command, shell=True, check=True)
                except Exception as e:
                    print(f"{Colours.WARNING}Error{Colours.END} executing command: {e}")
            except KeyboardInterrupt:
                print("Exiting...")
                sys.exit(0)


if __name__ == "__main__":
    main()
