
"""
Install libraries as needed

# !pip install langchain
# !pip install openai
# !pip install PyPDF2
# !pip install faiss-cpu
# !pip install tiktoken
# !Pip install gTTS  -- Text to Speech
# !pip install transformers Speech to Text

# !pip install playsound # pip install --upgrade wheel
# 

# NLTK
"""

from io import BytesIO
import time
from PyPDF2 import PdfReader, PdfMerger, PdfFileMerger
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from gtts import gTTS
import gradio as gr
import playsound
import os

# todo: need to externalize.
folder_path="C:\Work\Hackathon\Data\\"
out_file="out.pdf"
os.environ["OPENAI_API_KEY"]="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"

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
    pdf_merger.write(os.path.join(folder_path,out_file))    
    return pdf_merger

# Generate audio file from text
def speak(text, language='en'):
    # audio = BytesIO()
    tts = gTTS(text, lang=language)
    voice_file = os.path.join(folder_path, 'voice.mp3')
    tts.save(voice_file)
    playsound.playsound(voice_file)
    # os.remove(audio)
    return 

# def speak(text, language='en'):
#         mp3_file_object = BytesIO()
#         tts = gTTS(text, lang='en')
#         tts.write_to_fp(mp3_file_object)
#         pygame.init()
#         pygame.mixer.init()
#         pygame.mixer.music.load(mp3_file_object, 'mp3')
#         pygame.mixer.music.play()

# Create KB file

# fucntion to take in the query and return the outpout.
def chatbot(query, is_voice) :
    response = 'Hello world'
    if is_voice: 
        speak(response)
    return response

print("Creating lUI Interface...")
# ui = gr.Interface(fn=chatbot, inputs=[gr.inputs.Textbox(lines=5, label="Customer Call Center"),
#                                        gr.inputs.Checkbox(label="Enable Voice Readout")],       outputs='text', title="ACE Intelligent Assistant",     allow_flagging="manual",
#                                        flagging_options=["Incorrect Response", "Inappropriate Response", "other Reason"])

def flip_text(x):
    return x[::-1]
demo = gr.Blocks()


def transcribe(audio, state=""):
    return state, state

with demo:
    gr.Markdown("ACE The intelligent Assistanat")
    with gr.Tabs():
        with gr.TabItem("Text based"):
            with gr.Row():
                with gr.Column():
                    qyery_input = gr.TextArea(label='Question')
                    voice_flag = gr.Checkbox(label='Enable voice output')
                    submit_button = gr.Button("Submit")  
                with gr.Column():
                    answer_output = gr.TextArea(label='Answer')
                    with gr.Row():
                        flag_1 = gr.Button("Flag Incorrect Reponse")
                # with gr.Column():
                        flag_2 = gr.Button("Flag Inappropriate Reponse")
                # with gr.Column():
                        flag_3 = gr.Button("Flag Other Reponse")

           
        with gr.TabItem("Audio"):
            with gr.Row():
                audio_input = gr.Audio(source="microphone", type="filepath"), 
                text_output = gr.Textbox(label='Answer',)
                # audio_input.stream(fn=transcribe, inputs=[audio_input, state], outputs=[text_output, state])
                audio_output2 = gr.Checkbox(label='Enable voice output')
                text_button2 = gr.Button("Submit")  

    # Feedback logger
    flag_logger = gr.CSVLogger()                      
    flag_logger.setup([qyery_input, answer_output, flag_1], "Flagged reponses")
    flag_1.click(lambda *args: flag_logger.flag(args), [qyery_input, answer_output, flag_1], None, preprocess=False)
    flag_2.click(lambda *args: flag_logger.flag(args), [qyery_input, answer_output, flag_2], None, preprocess=False)
    flag_3.click(lambda *args: flag_logger.flag(args), [qyery_input, answer_output, flag_3], None, preprocess=False)
demo.launch()
