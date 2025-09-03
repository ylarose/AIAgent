import boto3
import os
from datetime import datetime

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain.chains.api import open_meteo_docs
from langchain.chains import APIChain, LLMChain
from langchain.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain.globals import set_debug

from langchain_community.utilities import OpenWeatherMapAPIWrapper

from bedrock_ai import init_model

from mytools import multiply, divide, getRealTimeValues, sendMail

# init model, from AWS Bedrock. Tested with several model, it seems not all can use agents or tools
def init_model2():

    # get AWS Bedrock key from config file, and set it as env variable
    with open("config.json") as config_file:
        config = json.load(config_file)
    aws_key = config['AWS_BEARER_TOKEN_BEDROCK'] 
    os.environ['AWS_BEARER_TOKEN_BEDROCK'] = aws_key
    
    # model_titan = "amazon.titan-text-express-v1" # This model doesn't support tool use.
    # model_llama32 = "eu.meta.llama3-2-3b-instruct-v1:0"  # This model doesn't support tool use
    model_claude_sonnet = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    model = init_chat_model(model_claude_sonnet, model_provider="bedrock_converse", temperature=0)
    print(f"model = {model}")
    
    return model


def test_model(model): 
    print("Asking LLM (no tools) to multiply 57 and 341. Expected: 19,437")
    query = "Please multiply 57 and 341"
    response = model.invoke([{"role": "user", "content": query}])
    response.pretty_print()


def run_agent(model):
    # set_debug(True)

    # list of tools available to agent
    tools = [multiply, divide, getRealTimeValues, sendMail]
    
    # create agent with model and tool list
    agent_executor = create_react_agent(model, tools)

    input_message = {"role": "user", "content": "Hi!"}

    # test it with multiple questions
    # "For our customer CATS, how many agents are currently connected?"
    listQuestions = ["What is the name of the first president of the USA?", "Please multiply 57 and 341", "For our customer CATS, if more than 2000 agents are connected, send a congratulation email to olivier.isidor@odigo.com"]
    
    # for each question: ask the agent
    for question in listQuestions:
        input_message = {"role": "user", "content": question}
        response = agent_executor.invoke({"messages": [input_message]}, verbose= False)
        for message in response["messages"]:
            message.pretty_print()


# test simple agent with weather
def test_simple_agent(model):

    # key is invalid...
    os.environ["OPENWEATHERMAP_API_KEY"] = ""
    weather = OpenWeatherMapAPIWrapper()
    weather_data = weather.run("London,GB")
    print(weather_data)

    question = "What is the current weather in Paris, France?"

    # only tool is weather
    tools = [weather.run]
    agent = create_react_agent(model, tools)

    input_message = {
        "role": "user",
        "content": question
    }

    for step in agent.stream(
        {"messages": [input_message]},
        stream_mode="values", verbose= True
    ):
        step["messages"][-1].pretty_print()
    
    return
    
    
# init model, using anthropic's Claude, through AWS bedrock
model = init_model()
# test_simple_agent(model)

# test model on its own, without agent or tool
test_model(model)

# finally create and run agent, with multiple tools
print("\n--- Now running Agent ---\n")
run_agent(model)

