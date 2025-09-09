# Simple HTTP Server. does not support https
# needs python3 and Flask library
# serves all supportTools webservices (/getDRGDetails, /getConversation, ...)

# to test offline, uncomment lines with after: "for offline tests"

from flask import Flask, render_template, request, send_from_directory, jsonify, abort

import sys
import time
from datetime import datetime, timedelta
from bedrock_ai import init_model
from open_ai import init_model_openAI
from agent_server import init_agent, ask_question

app = Flask(__name__)

app.Debug = True

# global variable to store agent
G_AGENT = None

def log(text):
    now = datetime.now()
    strDT = now.strftime("%Y-%m-%d, %H:%M:%S")
    print(f"{strDT} - {text}")

# path to files to parse

@app.route('/')
def index():
    log('Got /')
    return 'Hello world!'


@app.route('/<path:path>')
def getFile(path):
    # only accept extension in: .html, .js, .jpg
    log('Getting file: ' + path)
    str = ""
    if path.endswith(".html") or path.endswith(".js") or path.endswith(".jpg") or path.endswith(".svg") or path.endswith(".mp3") or path.endswith(".gif") or path.endswith(".ico") or path.endswith(".css") or path.endswith(".png"):
        str = send_from_directory('', path)
    else:
        log('File type not supported: ' + path)
        # awslogger.addlog('Getting file: ' + path)
        str = "<h2>File not supported</h2>"

    return str

# setup agent and LLM, returns first question
@app.route('/setupagent', methods=['GET', 'POST'])
def setupAgent():
    global G_AGENT

    log('In /setupAgent')
    jsdata = None
    
    instructions = request.form.get('instructions')
    log(f"instructions: {instructions[0:50]}...")
  
    # init LLM model
    model = init_model()
    # model = init_model_openAI()
    print(model)
    
    # now, init agent with instructions
    agent, response = init_agent(model, instructions)
    G_AGENT = agent
    log(f"got answer {response[0:50]}...")
    
    jsdata = jsonify(response)
        
    return jsdata


# get details of conversation, with server, convID, date, time
@app.route('/askquestion', methods=['GET', 'POST'])
def askQuestion():
    global G_AGENT
    
    log('In /askQuestion')
    
    question = request.form.get('question')
    
    log(f"question: {question[0:50]}...")
    response = ask_question(G_AGENT, question)
    log(f"response: {response[0:50]}...")
    
    jsdata = jsonify(response) 
        
    return jsdata


if __name__ == '__main__':
  
    # print('Argument List:', str(sys.argv))
    if (len(sys.argv) > 1):
        globalPath = sys.argv[1]

    # app.logger.setLevel(logging.INFO)
    log("Starting httpserver.py")
    
    app.run(debug=True, host='0.0.0.0', port=8080)


