# bedrock_ai
import os
import json     # to get env variables stored in config.json

from langchain_community.embeddings import BedrockEmbeddings
from langchain_aws import BedrockEmbeddings
from langchain.chat_models import init_chat_model

import boto3

MODEL_ID_CLAUDE = "anthropic.claude-3-sonnet-20240229-v1:0"
MODEL_ID_TITAN = "amazon.titan-embed-text-v2:0"
LANGSMITH_API_KEY_ID = "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"

def setenv():
    # get AWS Bedrock key from config file, and set it as env variable
    with open("config.json") as config_file:
        config = json.load(config_file)
    aws_key = config['AWS_BEARER_TOKEN_BEDROCK'] 
    print(aws_key[0:10])
    os.environ['AWS_BEARER_TOKEN_BEDROCK'] = aws_key
    
# init model, from AWS Bedrock. Tested with several model, it seems not all can use agents or tools
def init_model():

    setenv()
    
    # model_titan = "amazon.titan-text-express-v1" # This model doesn't support tool use.
    # model_llama32 = "eu.meta.llama3-2-3b-instruct-v1:0"  # This model doesn't support tool use
    model_id = MODEL_ID_CLAUDE
    
    model = init_chat_model(model_id, model_provider="bedrock_converse", temperature=0.2)
    # print(model)
    return model


def get_embeddings():
    import json     # to get env variables stored in config.json

    #"bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
    #bedrock_embeddings = BedrockEmbeddings(model_id=MODEL_ID, client=bedrock_client)
    # embeddings = BedrockEmbeddings(model_id=MODEL_ID, credentials_profile_name="ylarose-trial5", region_name="eu-west-3")

    setenv()
    MODEL_ID_TITAN = "amazon.titan-embed-text-v2:0"
    bedrock = boto3.client(service_name='bedrock-runtime')
    # embeddings = BedrockEmbeddings(model_id=MODEL_ID,client=bedrock)
    embeddings = BedrockEmbeddings(client=bedrock, credentials_profile_name="ylarose-trial5", region_name="eu-west-3", model_id=MODEL_ID_TITAN)
    
    return embeddings
    
