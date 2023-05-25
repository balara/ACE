# !pip install langchain
# !pip install openai
# !pip install PyPDF2
# !pip install faiss-cpu
# !pip install tiktoken
# !Pip install gTTS
# !pip install playsound # pip install --upgrade wheel
# !pip install gradio
# !pip install Flask 

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import openai

import os
from dotenv import dotenv_values

from flask import Flask
from flask import Flask, request, jsonify


# load env
env_vars = dotenv_values("/home/hackathonuser/hackathon/src/config/.env")
os.environ["OPENAI_API_KEY"]=env_vars.get('OPENAI_API_KEY')


# OpenAI setttings
openai.api_type = env_vars.get('API_TYPE')
openai.api_version = env_vars.get('API_VERSION')
openai.api_base = env_vars.get('OPENAI_API_BASE')
openai.api_key = env_vars.get('OPENAI_API_KEY')


# Program paramerters
vector_db_file =env_vars.get('VECTOR_DB')
embedding_deployment=env_vars.get('EMBEDDING_DEPLOYMENT')
embedding_model=env_vars.get('EMBEDDING_MODEL')
engine=env_vars.get('ENGINE')

http_port = env_vars.get("API_PORT")

# fucntion to take in the query and return the outpout.
def chatbot(query) :
    # Download embeddings from OpenAI
    embeddings = OpenAIEmbeddings(deployment="acetextembeddingsada002", model='text-embedding-ada-002', chunk_size=1)
    print('Loaidng the semantics from local Vector store...')
    vdb = FAISS.load_local(vector_db_file, embeddings)
    print('Searching the simnatics for the similartiy...')
    docs = vdb.similarity_search(query)

    print("Creating langchain QA Chain  ...")
    chain = load_qa_chain(OpenAI( engine='acedavinci003', temperature=0), chain_type="stuff")

    print("Calling Open API LLM to generate the answer ...")
    response = chain.run(input_documents=docs, question=query)
    return response


# API to reutn the cureated response for the question
app = Flask("ACE Hacathon Demo")
@app.route('/ace', methods=['GET'])
def query_records():
    question_str = request.args.get('question')
    answer_str = chatbot(question_str)
    print('Questions ->' + question_str+ ' Answer -> '+ answer_str )
    return jsonify({'question': question_str,
                    'answer':answer_str})
    app.run(host='0.0.0.0')
