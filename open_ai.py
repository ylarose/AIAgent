# scripts to initialize an OpenAI chat model
import os
import json     # to get env variables stored in config.json

from langchain_openai import ChatOpenAI


def setenv():
    # get AWS Bedrock key from config file, and set it as env variable
    with open("config.json") as config_file:
        config = json.load(config_file)
    aws_key = config['OPENAI_API_KEY'] 

    os.environ['OPENAI_API_KEY'] = aws_key
   
    
# init_model open OpenAI
def init_model_openAI():
    # set env variable for OpenAI key
    setenv()
    
    model = ChatOpenAI(temperature=0.2, model="gpt-5-nano")
    
    return model
    

def unit_test():
    # mod = init_model2()
    mod = init_model_openAI()

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
    
# unit_test()
 