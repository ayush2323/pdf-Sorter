from PyPDF2 import PdfReader
import streamlit as st
from transformers import pipeline
import io
import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_text_streamlit(prompt, text_area_placeholder=None,
                                   temperature=0.5,
                                   max_tokens=3000, top_p=1, frequency_penalty=0,
                                   presence_penalty=0, stream=True, html=False):

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt])
    return response.text
    # st.write(response.text, unsafe_allow_html=True)


st.title("PDF Sorter")

output_folder = "Organized"

files = st.file_uploader("Choose a PDF", type=["pdf"])

if st.button("Organize PDF"):
  with st.spinner('Working on PDFs'):
    pdf_data = io.BytesIO(files.read())
    reader = PdfReader(pdf_data)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]  # Currently processes only the first page
    raw_text = page.extract_text()

    ## Get the title and keywords ##
    output_format = 'title - keyword - keyword-....'
    
    # User interface
    prompt = ("Below is the text of a research paper. I want you to generate a name for the papers that has "
                      "the full name of the paper as well as 3 keywords that will allow me to find it later."
                      "If there are any special characters in the text like : / \ or other, remove them from title "
                      "Give raw text as the output") + \
                     "use the following format: " + output_format + \
                     f'"""{raw_text}"""'
 
    generated_text = generate_text_streamlit(prompt, max_tokens=40)
    # st.write(generated_text)
    # cleaned_text = ''.join(c for c in generated_text if c.isalnum() or c in [' ', '-', '_'])
 
    # st.subheader(f"PDF {i + 1}")
    st.write("Title:"+generated_text)
 
    ## Save the Files ##
    os.makedirs(output_folder, exist_ok=True)  # This creates the directory if it does not exist
    new_file_path = f"{output_folder}/{generated_text}.pdf"
 
    # Write the uploaded file to the new location
    with open(new_file_path, "wb") as f:
        # If the file object is from Streamlit, you should have access to getbuffer()
      f.write(files.getbuffer())
