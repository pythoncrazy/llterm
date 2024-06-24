from langchain_nvidia_ai_endpoints import (
    ChatNVIDIA,
)  # used for the actual NIM model itself
import platform
from llterm.code_parser import code_parser
import json


class LLM:
    def __init__(self, api_key, model_name, max_tokens, temperature):
        self.llm = ChatNVIDIA(
            model=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=api_key,
        )  # The LLM that we send messages to
        self.plaform_information = ""
        if platform.system() == "Linux":
            info = platform.freedesktop_os_release()
            self.plaform_string = f"The system the shell command will be executed on is {platform.system()} {platform.release()}, running {info.get('ID')} version {info.get('VERSION_ID', info.get('BUILD_ID'))}."
        else:
            self.plaform_string = f"The system the shell command will be executed on is {platform.system()} {platform.release()}."
        self.prior_messages = (
            []
        )  # With each new update being in the form [USER_MESSAGE, MODEL_RESPONSE]
        self.prompt = (
            """You are an expert at using shell commands. I need you to provide a response in the format `{"command": "your_shell_command_here"}`. """
            + self.plaform_information
            + """ Only provide a single executable line of shell code as the value for the "command" key. Never output any text outside the JSON structure. The command will be directly executed in a shell. For example, if I ask to display the message 'Hello, World!', you should respond with {"command": "echo 'Hello, World!'"}."""
        )

    def get_commands(self, user_message):
        # Taken mainly from: https://python.langchain.com/v0.2/docs/integrations/chat/nvidia_ai_endpoints/#working-with-nvidia-api-catalog
        response = self.llm.invoke(self.prompt + f"Here's what I'm trying to do: {user_message}. Only respond with the command").content
        commands = []
        for msg in response:
            try:
                json_content = code_parser(response)
                command_json = json.loads(json_content)
                command = command_json.get("command", "")
                if command:  # Ensure the command is not empty
                    commands.append(command)
            except json.JSONDecodeError:
                # Fallback: treat the message as a command
                commands.append(response)

        # Deduplicate commands
        commands = list(set(commands))
        return commands
        