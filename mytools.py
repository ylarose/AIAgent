from langchain_core.tools import tool

# for weather tools
import requests
import json

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """divide  two numbers."""
    return float(a / b)

@tool
def getRealTimeValues(customer: str, valueType: str) -> int:
    """ takes two arguments: customer name, and valueType, both as strings
        if valuetype is "calls", the function returns the number of ongoing calls for this customer, in real time
        if valuetype is "agent", the function returns the number of currently connected agents, in real time
    """
    if customer == "CATS":
        if valueType == "agent":
            return 3000
        if valueType == "calls":
            return 500
    if customer == "SmallOne":
        return 10

@tool
def sendMail(dest: str, content: str) -> str:
    """ function to send email
        it takes two arguments: dest which represents the person or system we want to which we sending the mail,
        and content, which represents the content of the email
    """
    print(f"sending to {dest} the mail: {content}") 
    return "sendMail(dest, content) OK"
    
@tool
def createTicket(typeOfPhone: str, refNumber: str) -> str:
    """ this function creates a service ticket, it takes two arguments: typeOfPhone and refNumber
        the first argument corresponds to the tpe of iPhone (iPhone 14 or iPhone 15)
        the second argument corresponds to the reference number of the iPhone
        the functoin returns a ticket number, that can be given to the customer
    """
    print(f"creating ticket in ServiceNow for {typeOfPhone} and {refNumber}")
    
    return "INC0012345"


@tool
def getWeather(latitude: str, longitude: str) -> str:
    """
    This function gets current weather data for a given location. It takes 2 parameters: the latitude and the longitude of the location, and returns a JSON string containing the current weather at the location
    """
    
    dictResp = None
    strURL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    headers1 = {'Content-Type': 'application/json'}
    
    # sending post request and saving response as response dict 
    try:
        resp = requests.get(strURL, headers=headers1) 
        # print("sendRequest.resp: %s" % resp.text)
        if (resp.status_code == 200):
            dictResp = json.loads(resp.text)       
            # print(dictResp)
        else:
            print("sendRequest HTTP Status: %d - %s" % (resp.status_code, resp.reason))
            print("URL: " + strURL)
            # print(resp)
    
    except Exception as ex:
        print(ex)
    
    return dictResp
