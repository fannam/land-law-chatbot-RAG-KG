from langchain.prompts.prompt import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings
from langchain_community.vectorstores.faiss import FAISS

def create_prompt(template):
    try:
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        return prompt
    except Exception as e:
        print(f"Error creating prompt: {e}")
        return None

def read_vector_db(vector_db_path):
    try:
        model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
        gpt4all_kwargs = {'allow_download': 'True'}
        embedding_model = GPT4AllEmbeddings(model_name=model_name, gpt4all_kwargs=gpt4all_kwargs)
        db = FAISS.load_local(vector_db_path, embedding_model, allow_dangerous_deserialization=True)
        return db
    except Exception as e:
        print(f"Error reading vector database: {e}")
        return None

def create_qa_chain(prompt, llm, db):
    try:
        llm_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=False,
            chain_type_kwargs={'prompt': prompt}
        )
        return llm_chain
    except Exception as e:
        print(f"Error creating QA chain: {e}")
        return None

def response_by_vector_search(question, prompt, llm, db):
    try:
        llm_chain = create_qa_chain(prompt, llm, db)
        if llm_chain is None:
            return "Error in creating QA chain"
        response = llm_chain.invoke({"query": question})
        print(f"vector: {response}")
        return response['result']
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Error generating response"
