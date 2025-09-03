from datetime import datetime
from typing_extensions import List, TypedDict
import os

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.documents import Document
from langchain import hub
from langgraph.graph import START, StateGraph

from bedrock_ai import init_model, get_embeddings

# pointer to InMemory vector store
G_VECTOR_STORE = None

# load documents into vector_store, and return vector_store
def load_documents():
    csv_file_path = "customer_data.csv"
    loader = CSVLoader(file_path=csv_file_path)
    documents = loader.load()
    # print(documents)
    
    try:
        vector_store = InMemoryVectorStore(get_embeddings())
        t1 = datetime.now()
        print("Loading documents...")
        vector_store.add_documents(documents=documents)
        t2 = datetime.now()
        print("Imported CSV file took: " + str(t2-t1))
        
    except Exception as e:
        print(e)
        
    return vector_store

def test_vector():
    vector_store = load_documents()
    results = vector_store.similarity_search(query="HMRC",k=2)
    for doc in results:
        print(f"* {doc.page_content} [{doc.metadata}]")

    return
    

# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    global G_VECTOR_STORE
    
    retrieved_docs = G_VECTOR_STORE.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    # N.B. for non-US LangSmith endpoints, you may need to specify
    # api_url="https://api.smith.langchain.com" in hub.pull.
    prompt = hub.pull("rlm/rag-prompt")


    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    model = init_model()
    response = model.invoke(messages)
    return {"answer": response.content}

# define RAG graph
def define_graph():

    # Compile application and test
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    return graph
    

G_VECTOR_STORE = load_documents()

# necessary for LangSmith, included in LangGraph
os.environ['LANGSMITH_API_KEY'] = "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"
os.environ['LANGSMITH_TRACING'] = "true"

# create graph, with 2 nodes: retrieve and generate
graph = define_graph()

# For terminal/ASCII output:
# graph.get_graph().draw_ascii() # needs grandalf library

question = "How many inbound calls does HMRC make?"
print(f"User Question : {question}")
response = graph.invoke({"question": question})
print(response["answer"])

question = "Which customer is making the most calls?"
print(f"User Question : {question}")
response = graph.invoke({"question": question})
print(response["answer"])

