from flask import Flask, request, jsonify, send_from_directory
from langchain_openai import ChatOpenAI
from graph_search import response_by_graph_search
from vector_search import read_vector_db, response_by_vector_search, create_prompt
from langchain_core.messages.base import BaseMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
import os

# Load the vector database
vector_db_path = "vectordbstore"
db = read_vector_db(vector_db_path)

app = Flask(__name__, static_folder='static')

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = ""

# Initialize ChatGPT model
chatgpt = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def combine_vector_and_graph_search(user_message, response_vector, response_graph):
    system_prompt = f"""You are a helpful assistant. Answer this question with these informations. 
    {user_message}
    This source of information is correct: 
    {response_graph}. 
    The secondary source contains this additional information: 
    {response_vector}. 
    Create a response in Vietnamese natural language based on these two informations. Prioritize the primary source, only use the secondary source if it has additional meaning for the response.
    """

    
    # Create the chat prompt as a list of messages
    prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    
    # Generate a response using the ChatGPT model
    response = chatgpt.invoke(prompt)
    #print(response)
    return response.content

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/chat', methods=['POST'])
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    template = """You are a helpful assistant. Use the following context to answer the question at the end. 
    Context: {context}
    Question: {question}
    Answer:"""
    prompt = create_prompt(template)
    
    if not user_message:
        return jsonify({'reply': 'No message received'}), 400
    
    try:
        # Uncomment the following line to use vector search
        response_vector = response_by_vector_search(user_message, prompt, chatgpt, db)
        print(response_by_vector_search)
        #response_vector = "No useful information"
        response_graph = response_by_graph_search(user_message, chatgpt)
        final_response = combine_vector_and_graph_search(user_message, response_vector, response_graph)
        
        return jsonify({'reply': final_response})
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")
        return jsonify({'reply': 'An unexpected error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
