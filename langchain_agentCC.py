import boto3
import os
from datetime import datetime

from langchain.chat_models import init_chat_model

from langchain.chains.api import open_meteo_docs
from langchain.chains import APIChain, LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from langchain_core.messages import HumanMessage

from langchain.globals import set_debug

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from bedrock_ai import init_model

from mytools import createTicket


def test_model(model): 
    print("Asking LLM (no tools) to multiply 57 and 341. Expected: 19,437")
    query = "Please multiply 57 and 341"
    response = model.invoke([{"role": "user", "content": query}])
    response.pretty_print()


# using pretty print to print output from agent or tools
def print_output(chunk):
    
    if chunk is None:
        return
    
    # chunk format: chunck: {'agent': {'messages': [AIMessage(content="I'm sorry to hear you've lost your iPhone. Let me first ask, what model of iPhone do you have? I can assist with iPhone 14 and iPhone 15 models.", additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': 'a19d798b-7b4c-4a7f-b491-d6ac7d751ed9', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Mon, 01 Sep 2025 07:00:20 GMT', 'content-type': 'application/json', 'content-length': '328', 'connection': 'keep-alive', 'x-amzn-requestid': 'a19d798b-7b4c-4a7f-b491-d6ac7d751ed9'}, 'RetryAttempts': 0}, 'stopReason': 'end_turn', 'metrics': {'latencyMs': [1069]}, 'model_name': 'anthropic.claude-3-sonnet-20240229-v1:0'}, id='run--4d12f89e-b8d5-4dbd-b8a8-6a81aa60e7a9-0', usage_metadata={'input_tokens': 492, 'output_tokens': 42, 'total_tokens': 534, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}})]}}
    # output can come from agent or from tool
    if 'agent' in chunk.keys():
        print(chunk['agent']['messages'][0].pretty_print())
    elif 'tools' in chunk.keys():
        print(chunk['tools']['messages'][0].pretty_print())    
    else:
        print(chunk)
    print('------')
    

# test a question and answer agent
def question_agent(model):
    
    # memory pointer
    memory = InMemorySaver()
    # graph = graph_builder.compile(checkpointer=memory)
    config = {"configurable": {"thread_id": "1"}}

    # list of tools available to agent
    tools = [createTicket]
    
    # create agent with model and tool list
    agent_executor = create_react_agent(model, tools, checkpointer=memory)

    # giving general instructions to the model
    instruction_GB = """Your name is Bob, you speak english, your are helping customers having issues with their iPhones
        The only iPhone types supported by you are: iPhone 14 and iPhone 15.
        If the customer's iPhone type is different, apologize and tell them you will forward their request to an agent.
        If the customer's iPhone type is 14 or 15, ask them if the iPhone is damaged or lost.
        if the customer iPhone is damaged or lost, ask for the reference number, found in the email they have received.
        Finally, create a ticket using the createTicket tool, and give the customer the ticket number returned by the tool.
        To end conversation, whish the customer a very happy day.
        """

    instruction_FR = """Votre nom est Jean, vous parlez et comprenez le francais, et vous etes un agent qui aid eles clients ayant des problèmes avec leurs iPhone.
        Les seuls modeles supportés sont les iPhone 14 et 15.
        Si le client a un iPhone 14 ou 15, il faut leur demander si leur iPhone est perdu ou abimé.
        Si le client a un iPhone qui n'est pas un model 14 ou 15, propsez leur de parler a un agent
        Si le client a un iPhone 14 ou 15, abimé ou perdu, il faut créer un ticket par l'outil createTicket, en passant le type d'iPhone 
        et la référence de l'iPhone. Le client peut trouver la référence dans l'email qui lui a été envoyé lors de l'achat
        Pour finir, souhaitez une bonne journée au client, en le remerciant de vous avoir contacté
        """
   
    for chunk in agent_executor.stream({"messages": [HumanMessage(content=instruction_GB)]}, config):
        # chunk format : {'agent': {'messages': [AIMessage(content="Hi Yanick, my name is Claude. It's nice to meet you!", additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': 'd57be8da-188b-4f73-b8d9-379c1310d4ce', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Sat, 30 Aug 2025 18:22:05 GMT', 'content-type': 'application/json', 'content-length': '235', 'connection': 'keep-alive', 'x-amzn-requestid': 'd57be8da-188b-4f73-b8d9-379c1310d4ce'}, 'RetryAttempts': 0}, 'stopReason': 'end_turn', 'metrics': {'latencyMs': [726]}, 'model_name': 'anthropic.claude-3-sonnet-20240229-v1:0'}, id='run--f0cdf087-ebab-40d8-a51a-e02dbc642c2f-0', usage_metadata={'input_tokens': 535, 'output_tokens': 20, 'total_tokens': 555, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}})]}}
        # chunk.pretty_print()
        print_output(chunk)
    
    # The config is the **second positional argument** to stream() or invoke()!
    question = ""
    while True:
        question = input("Your input: ")
        # input_message = {"role": "user", "content": question}
        if question.lower().startswith('quit'):
            exit()
        
        for chunk in agent_executor.stream({"messages": [HumanMessage(content=question)]}, config):
            # chunk format : {'agent': {'messages': [AIMessage(content="Hi Yanick, my name is Claude. It's nice to meet you!", additional_kwargs={}, response_metadata={'ResponseMetadata': {'RequestId': 'd57be8da-188b-4f73-b8d9-379c1310d4ce', 'HTTPStatusCode': 200, 'HTTPHeaders': {'date': 'Sat, 30 Aug 2025 18:22:05 GMT', 'content-type': 'application/json', 'content-length': '235', 'connection': 'keep-alive', 'x-amzn-requestid': 'd57be8da-188b-4f73-b8d9-379c1310d4ce'}, 'RetryAttempts': 0}, 'stopReason': 'end_turn', 'metrics': {'latencyMs': [726]}, 'model_name': 'anthropic.claude-3-sonnet-20240229-v1:0'}, id='run--f0cdf087-ebab-40d8-a51a-e02dbc642c2f-0', usage_metadata={'input_tokens': 535, 'output_tokens': 20, 'total_tokens': 555, 'input_token_details': {'cache_creation': 0, 'cache_read': 0}})]}}
            print_output(chunk)


# init model, using anthropic's Claude, through AWS bedrock
model = init_model()

# finally create and run agent, with multiple tools
question_agent(model)
