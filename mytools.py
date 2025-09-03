from langchain_core.tools import tool

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
