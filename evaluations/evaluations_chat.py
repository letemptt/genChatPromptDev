
import os
import sys
import json
import pandas as pd
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.evals.evaluators import CoherenceEvaluator, RelevanceEvaluator 
from promptflow.evals.evaluate import evaluate

sys.path.append('/Users/toniletempt/Projects/GENCHATPROMPTDEV/code')
from chatquestiongen import get_response
#from chatquestiongen import get_response
from dotenv import load_dotenv
load_dotenv()



if __name__ == '__main__':
    # Initialize Azure OpenAI Connection
    model_config = AzureOpenAIModelConfiguration(
            azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
    
    # set the path to the data file to use for evaluations
    data_path = "/Users/toniletempt/Projects/genChatPromptDev/travelchatresults0729-gtp35.jsonl"

    # Check if the file exists and is not empty
    if os.path.isfile(data_path) and os.path.getsize(data_path) > 0:
        # Read the JSON lines file into a pandas DataFrame
        df = pd.read_json(data_path, lines=True)
        df.head()
    else:
        print(f"No data found at {data_path}")

    # Create evaluators for different evaluation metrics
    #relevance_evaluator = RelevanceEvaluator(model_config)
    #groundedness_evaluator = GroundednessEvaluator(model_config)
    #fluency_evaluator = FluencyEvaluator(model_config)
    coherence_evaluator = CoherenceEvaluator(model_config=model_config)
    relevance_evaluator = RelevanceEvaluator(model_config=model_config)

    # Perform evaluation using the evaluate function
    path = "/Users/toniletempt/Projects/genChatPromptDev/travelchatresults0729-gtp35.jsonl"
    result = evaluate(
        data=path,
       # target=get_response,
        evaluators={
            "coherence": coherence_evaluator,
            "relevance": relevance_evaluator
           # "fluency": fluency_evaluator,
           # "groundedness": groundedness_evaluator,
        },
        evaluator_config={
            "coherence": {
                "answer": "${data.Answer}",
                "question": "${data.Question}"
            },
            "relevance": {
                "answer": "${data.Answer}",
                "context": "${data.Context}",
                "question": "${data.Question}",
            }
        }
    )
    
    # # Print result_eval to json file
    # with open('result_eval.json', 'w') as f:
    #     json.dump(result_eval, f)

    # Convert the evaluation results to a pandas DataFrame
    eval_result = pd.DataFrame(result["rows"])
    print(eval_result)