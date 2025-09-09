# implements a LangChain agent as a server. To be used by a webserver
import os
from datetime import datetime

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from bedrock_ai import init_model       # , init_model2

from mytools import createTicket, sendMail, lookupMail

# giving general instructions to the model
INSTRUCTION_GB = """Your name is Bob, you speak english, your are helping customers having issues with their iPhones
    The only iPhone types supported by you are: iPhone 14 and iPhone 15.
    If the customer's iPhone type is different, apologize and tell them you will forward their request to an agent.
    If the customer's iPhone type is 14 or 15, ask them if the iPhone is damaged or lost.
    if the customer iPhone is damaged or lost, ask for the reference number, found in the email they have received.
    Finally, create a ticket using the createTicket tool, send an email to the customer, and give the customer the ticket number returned by the tool.
    To end conversation, wish the customer a very happy day.
    If you feel that the customer gets upset or irritated, propose to forward the request to an agent
    """

INSTRUCTION_FR = """Votre nom est Jean, vous parlez et comprenez le francais, et vous etes un agent qui aid eles clients ayant des problèmes avec leurs iPhone.
    Les seuls modeles supportés sont les iPhone 14 et 15.
    Si le client a un iPhone 14 ou 15, il faut leur demander si leur iPhone est perdu ou abimé.
    Si le client a un iPhone qui n'est pas un model 14 ou 15, propsez leur de parler a un agent
    Si le client a un iPhone 14 ou 15, abimé ou perdu, il faut créer un ticket par l'outil createTicket, en passant le type d'iPhone 
    et la référence de l'iPhone. Le client peut trouver la référence dans l'email qui lui a été envoyé lors de l'achat
    Pour finir, souhaitez une bonne journée au client, en le remerciant de vous avoir contacté
    """

CONFIG = {"configurable": {"thread_id": "1"}}

# test a question and answer agent
def init_agent(model, instructions):
    resp = ""
    
    # memory pointer
    memory = InMemorySaver()

    # list of tools available to agent
    tools = [createTicket, sendMail, lookupMail ]
    
    # create agent with model and tlookupMailool list
    agent = create_react_agent(model, tools, checkpointer=memory)

    # sends message to agent and wait for answer
    for chunk in agent.stream({"messages": [HumanMessage(content=instructions)]}, CONFIG):
        # for initialisation, the data always come from the agent
        data = chunk['agent']['messages'][0].text()
        resp = resp + data  
    
    return agent, resp


# test a question and answer agent
def ask_question(agent, question):
    resp = ""    
    
    # sends message to agent and wait for answer
    for chunk in agent.stream({"messages": [HumanMessage(content=question)]}, CONFIG):
        # if the data comes from agent or tools, the text is in a different place
        # only send data returned by agent, not from tools
        if 'agent' in chunk.keys():
            data = chunk['agent']['messages'][0].text()
            print(f"data={data}")
            resp = resp + data
        elif 'tools' in chunk.keys():
            # data = chunk['tools']['messages'][0].text()
            print(f"Output from tool: {chunk['tools']['messages'][0].text()}")
    
    return resp 

### END OF CODE


### unit testing
def test_server():
    model = init_model2()
    print(model)
    agent, firstAnswer = init_agent(model, INSTRUCTION_GB)
    print(f"answer: {firstAnswer}")

    question = "Hi, my name is Axel, I just lost my iPhone"
    print(f"question: {question}")
    answer = ask_question(agent, question)
    print(f"answer: {answer}")

# test_server()
