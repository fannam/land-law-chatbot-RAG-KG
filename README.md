## What do I need?
1. You need a LLM, should be high performance such as Llama 2, Llama 3 or gpt-3.5. The model has to belong to Runnable class (has invoke method)
2. You need a Knowledge Graph
3. You need an embeddings model
4. You need to embedding the pdf text file to create a .pkl and .faiss file for vector search (this is the vector store a.k.a vector database - using CBOW technique )

## How can I use this chatbot 

1. Download requirements.txt file and save it somewhere in your computer
2. Using miniconda or anaconda to create a virtual environment (not necessary but recommend to use venv to remove whenever you want)
3. After activate the venv, type "cd path/to/your/file" with path/to/your/file is the folder which contain requirements.txt
4. Type "pip install -r requirements.txt" then press Enter and waiting for the libraries' installation
5. Download Chatbot web folder and open with Visual Studio Code
6. Select interpreter (ctrl + shift + P) for Chatbot web folder as the venv which you just created before
7. Run app.py and open in local host
8. If you want to use your own vector database, you have to remove my files in vectorstores folder and replace with your own vector database

