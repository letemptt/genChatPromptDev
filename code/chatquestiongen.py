import os
import csv
import sys
import json
import writecsv as writecsv
import writejson as writejson
from dotenv import load_dotenv
load_dotenv()
from openai import AzureOpenAI

from promptflow.core import Prompty, AzureOpenAIModelConfiguration

#from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def write_csv(output_file=None, question=None, answer=None, chat_context=None):
    try:
        with open(output_file, mode='a') as csvfile:
            #write rows
            writer = csv.writer(csvfile)
            writer.writerow([question, answer, chat_context])
    except Exception as e:
        print("failed to write csv file %s" % (e))
    return

def get_response():

    ### Setup variables
    output_file = os.getenv("CSV_FILE")
    jsonl_file = os.getenv("JSONL_FILE")
    header_list = ['question', 'answer', 'context']
    num_of_questions = os.getenv("NUM_OF_QUESTIONS")
    prompt_question = "Generate ", num_of_questions, " travel question for me."
    prompty_file = os.getenv("PROMPTY_FILE")
    #Write header for csv file
    #writecsv.write_header(output_file, header_list)

    model_config = AzureOpenAIModelConfiguration(
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    prompty = Prompty.load(prompty_file, model={'configuration': model_config})
    result = prompty(
        chat_history=[
            {"role": "user", "content": "Generate a travel question for me."},
            {"role": "assistant", "content": "What can I do in London for a weekend trip?"}
        ],
        chat_input=prompt_question)
    #print(result)
    result_list = result.split('\n')
    print(result.split('\n'))
    print("result_list:", result_list)
    for i in result_list:
        if i.split('.')[0].isdigit():
            question = i.split('.')[1]
            print("question:", question)
            write_csv(output_file, prompt_question, question, "What can I do in London for a weekend trip?")

    writejson.write_json(output_file, jsonl_file)
    return {"answer": result, "context": "What can I do in London for a weekend trip?"}
if __name__ == "__main__":
    get_response()