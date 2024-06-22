#!/home/supersketchy/miniforge-pypy3/envs/llm-term/bin/python
## MAKE SURE TO SET THE CORRECT SHEBANG, otherwise the executable file may not run

import os
from dotenv import (
    load_dotenv,
    set_key,
)  # used to set the various env variables (such as the api keys)
import getpass  # Get the key if not there
from langchain_nvidia_ai_endpoints import (
    ChatNVIDIA,
)  # used for the actual NIM model itself


load_dotenv()

# Taken from: https://python.langchain.com/v0.2/docs/integrations/chat/nvidia_ai_endpoints/
# # del os.environ['NVIDIA_API_KEY']  ## delete key and reset
if os.environ.get("NVIDIA_API_KEY", "").startswith("nvapi-"):
    api_key = os.environ.get("NVIDIA_API_KEY", "")
else:
    api_key = getpass.getpass("NVAPI Key (starts with nvapi-): ")
    assert api_key.startswith("nvapi-"), f"{api_key[:5]}... is not a valid key"
    os.environ["NVIDIA_API_KEY"] = api_key
    set_key(dotenv_path= './.env', key_to_set="NVIDIA_API_KEY", value_to_set=api_key)
if os.environ.get("MODEL") != "":
    model = "mistralai/mixtral-8x7b-instruct-v0.1"
else:
    model = os.environ.get("MODEL")

if os.environ.get("MAX_TOKENS") != "":
    max_tokens = 2
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


llm = ChatNVIDIA(model=model, max_tokens=max_tokens, temperature=temperature)
