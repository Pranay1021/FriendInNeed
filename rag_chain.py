# rag_engine.py
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain_community.embeddings import FastEmbedEmbeddings

# Initialize embeddings, vector DBs, LLM once (reused per request)
embedding = FastEmbedEmbeddings()
conversation_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding)
personal_info_db = Chroma(persist_directory="./personal_db", embedding_function=embedding)
llm = OllamaLLM(model="llama3")

# System prompt template
system_prompt = (
    "You are a helpful, honest assistant that answers based on the user's data."
    "I have provided you some data which contains information about interacting with mental health condition as well as some information about me. I am Pranay.\n"
    "Everytime you recieve a question, you should first look at the context provided and then answer the question based on that context.\n"
    "The query may be about my personal information or about the mental health.\n"
    "If the context does not contain enough information to answer the question, you should say that you don't know.\n"
    "You should not make up any information.\n"
    "Also while answering personal questions about me , answer like you are my friend. And if you do not know the answer, say that pranay hasnt told me about it.\n"
)

def query_rag(question: str) -> dict:
    # Search both databases
    conversation_docs = conversation_db.similarity_search(question, k=2)
    personal_docs = personal_info_db.similarity_search(question, k=2)

    # Combine context
    combined_context = "\n\n".join([doc.page_content for doc in personal_docs + conversation_docs])

    # Build prompt
    final_prompt = f"{system_prompt}\nContext:\n{combined_context}\n\nUser question:\n{question}"

    # Invoke LLM
    response = llm.invoke(final_prompt)

    return {
        "answer": response,
        "sources": [doc.page_content for doc in personal_docs + conversation_docs]
    }
