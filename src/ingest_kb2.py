
# 
# ##################  Program to Ingest the Knowldge base  #####################33
# 


"""
Install libraries as needed

# !pip install langchain
# !pip install openai
# !pip install PyPDF2
# !pip install faiss-cpu
# !pip install tiktoken
# !Pip install gTTS
# !pip install playsound # pip install --upgrade wheel
# !pip install gradio

# NLTK

#  aggregate pdf -> read pdf -> extreact text -> vectorize -> store in VDB -> read input query -> similarity seach -> pass search result to OPENAI  
"""


from PyPDF2 import PdfReader, PdfMerger, PdfFileMerger
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import openai
import os
from dotenv import dotenv_values


# load env
env_vars = dotenv_values("/home/hackathonuser/hackathon/src/config/.env")
os.environ["OPENAI_API_KEY"]=env_vars.get('OPENAI_API_KEY')

# OpenAI setttings
openai.api_type = env_vars.get('API_TYPE')
openai.api_version = env_vars.get('API_VERSION')
openai.api_base = env_vars.get('OPENAI_API_BASE')
openai.api_key = env_vars.get('OPENAI_API_KEY')
engine=env_vars.get('ENGINE')



# Program paramerters
vector_db_file =env_vars.get('VECTOR_DB')
embedding_deployment=env_vars.get('EMBEDDING_DEPLOYMENT')
embedding_model=env_vars.get('EMBEDDING_MODEL')
src_folder = env_vars.get('SRC_FOLDER')
out_file = env_vars.get('OUT_FILE')
# quit()

# Read the pdf files  the folder and return a concatinated PDF file.
def readKB(folder_path, out_file):

    # List of PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    # Sort the PDF files by name (optional)
    pdf_files.sort()

    # Create a PdfFileMerger object
    pdf_merger = PdfMerger()

    # Loop through the PDF files and append them to the merger object
    for pdf_file in pdf_files:
        pdf_file = open(os.path.join(folder_path, pdf_file), "rb")
        print("Merging... "+ pdf_file.name)
        pdf_reader = PdfReader(pdf_file)
        pdf_merger.append(pdf_reader)
    print("Merging Completed")
    pdf_file.close;
    print("Creationg merged KB file...")
    pdf_merger.write(out_file)    
    return pdf_merger

# read data from the file and put them into a variable called raw_text
def extreactText():
    print("reading merged KB  file...")
    kb_file = PdfReader(open(out_file, "rb"))
    print("extracing raw text from the pdf file..."+ str(len(kb_file.pages)))
    raw_text = ''
    print('extreacing page ', end= ' ')
    for i, page in enumerate(kb_file.pages):
        text = page.extract_text()
        if text:
            raw_text += text
        if i%100 ==0 :
            print('.',end= ' ')
    print
    print("Completed extracing raw text from the pdf file..."+ str(len(raw_text)))
    return raw_text

# We need to split the text that we read into smaller chunks so that during information retreival we don't hit the token size limits. 
def textSplitter(raw_text):
    print("Splitting the raw text file...")
    text_splitter = CharacterTextSplitter(        
        separator = "\n",
        chunk_size = 1200,
        chunk_overlap  = 200,
        length_function = len,
    )
    chunks = text_splitter.split_text(raw_text)
    print("Splited the raw text file to "+ str(len(chunks)) +" chunks ")
    return chunks

# Download embeddings
print("Creating embeddings...")
embeddings = OpenAIEmbeddings(deployment="acetextembeddingsada002", model='text-embedding-ada-002', chunk_size=1)
print("Creating embeddings... done.")


if os.path.isdir(vector_db_file) :
    print('reusing existing db data....')
    vdb = FAISS.load_local( vector_db_file, embeddings)

else :
    # Create KB file
    readKB(src_folder, out_file)
    text=extreactText()
    chunks = textSplitter(text)

    print('creating db data....')
    vdb = FAISS.from_texts(chunks, embeddings)
    vdb.save_local( vector_db_file)

print("Creating Knowledge DB done successfully")

