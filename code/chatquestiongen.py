import os
from dotenv import load_dotenv
load_dotenv()
from openai import AzureOpenAI

from promptflow.core import Prompty, AzureOpenAIModelConfiguration
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

model_config = AzureOpenAIModelConfiguration(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

prompty = Prompty.load("chatquestgen.prompty", model={'configuration': model_config})
result = prompty(
    chat_history=[
        {"role": "user", "content": "Generate a travel question for me."},
        {"role": "assistant", "content": "What can I do in London for a weekend trip?"}
    ],
    chat_input="Generate 10 travel questions for me.")

print(result)