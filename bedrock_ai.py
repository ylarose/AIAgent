# bedrock_ai
import os
import json     # to get env variables stored in config.json

from langchain_community.llms import OpenAI


from langchain_community.embeddings import BedrockEmbeddings
from langchain_aws import BedrockEmbeddings
from langchain.chat_models import init_chat_model

# for init2
from langchain_aws.chat_models import ChatBedrock
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from boto3 import _get_default_session
from boto3.session import Session
from mypy_boto3_bedrock_runtime.client import BedrockRuntimeClient


from pydantic import BaseModel, Field
from enum import Enum

import boto3

MODEL_ID_CLAUDE3 = "anthropic.claude-3-sonnet-20240229-v1:0"
MODEL_ID_CLAUDE37 = "eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
MODEL_ID_MISTRAL7B = "mistral.mistral-7b-instruct-v0:2"


MODEL_ID_TITAN = "amazon.titan-embed-text-v2:0"


def setenv():
    # get AWS Bedrock key from config file, and set it as env variable
    keys_ids = ['AWS_BEARER_TOKEN_BEDROCK', 'LANGSMITH_API_KEY_ID']
    for key_id in keys_ids:
        with open("config.json") as config_file:
            config = json.load(config_file)
            long_key = config[key_id] 
            # print(aws_key[0:10])
            os.environ[key_id] = long_key
      
    
# init model, from AWS Bedrock. Tested with several model, it seems not all can use agents or tools
def init_model():

    setenv()
    
    # model_titan = "amazon.titan-text-express-v1" # This model doesn't support tool use.
    # model_llama32 = "eu.meta.llama3-2-3b-instruct-v1:0"  # This model doesn't support tool use
    model_id = MODEL_ID_CLAUDE3
    
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
    
"""
# trying to access other more modern models, failing so far...
# for init2
def get_bedrock_client(region: str, profile: str | None = None) -> BedrockRuntimeClient:
    session = _get_default_session() if profile is None else Session(profile_name=profile)
    return session.client("bedrock-runtime", region_name=region)
    

class ModelId(str, Enum):
    CLAUDE_3_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
    CLAUDE_3_SONNET = "eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
    CLAUDE_4_SONNET = "eu.anthropic.claude-sonnet-4-20250514-v1:0"
    CLAUDE_3_OPUS = "anthropic.claude-3-opus-20240229-v1:0"
    MISTRAL_7B = "mistral.mistral-7b-instruct-v0:2"

class ModelKwargs(BaseModel):
    temperature: float = Field(default=0.5, ge=0, le=1)
    max_tokens: int = Field(default=2048, ge=1, le=4096)
    top_p: float = Field(default=0.999, ge=0, le=1)
    top_k: int = Field(default=0, ge=0, le=500)

def get_chat_bedrock(
    client: BedrockRuntimeClient,
        model_id: ModelId,
        model_kwargs: ModelKwargs,
        streaming: bool = False,
        verbose: bool = False) -> ChatBedrock:
            return ChatBedrock(
                client=client,
                region_name="eu-west-3",
                model_id=model_id.value,
                model_kwargs=model_kwargs.__dict__,
                streaming=streaming,
                verbose=verbose,
                callbacks=[StreamingStdOutCallbackHandler()] if streaming else []
            )


# init model, from AWS Bedrock, with boto3 client. 
def init_model2():    
    # client = get_bedrock_client("eu-west-3", "ylarose-trial5")
    client = get_bedrock_client("eu-west-3")
    print(client)
    
    # get a chat bedrock model
    chat_model = get_chat_bedrock(
        client=client,
        model_id=ModelId.CLAUDE_3_SONNET,
        model_kwargs=ModelKwargs(),
    )
    
    print(chat_model)
    return chat_model

"""

def unit_test():
    mod = init_model()
    # mod = init_model2()

    print(f"mod={mod}")
    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to French. Translate the user sentence.",
        ),
        ("human", "I love programming."),
    ]
    ai_msg = mod.invoke(messages)
    print(ai_msg)
    return
    
unit_test()
