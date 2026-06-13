from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
# from typer import prompt
load_dotenv()

Gemini_API_KEY = os.getenv('GEMINI_API_KEY')

if not Gemini_API_KEY:
    raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")

genai.configure(api_key=Gemini_API_KEY)
model = genai.GenerativeModel('gemini-3.5-flash')

def get_gemini_response(input_text, image):
    response = model.generate_content([input_text, image[0]])
    return getattr(response, "text", "No response received.")


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #REad the file in bytes
        bytes_data = uploaded_file.getvalue()
        image_part=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_part
    else:
        raise FileNotFoundError("No file uploaded. Please upload an invoice image to proceed.")
        
    
#Initialize our Streamlit app
st.set_page_config(page_title="AI Invoice Extractor", page_icon=":money_with_wings:")
st.title("AI Invoice Extractor")

st.header("Extract text from invoice images")
input=st.text_input("Enter your query about the invoice (e.g., 'What is the total amount?')","", key="input")
uploaded_file = st.file_uploader("Upload an invoice image", type=["jpg", "jpeg", "png"])    
submit_button = st.button("Tell me about the invoice")
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption='Uploaded Invoice Image', use_column_width=True)
    


system_prompt="""You are an AI assistant that extracts key information from invoice images.
Please analyze the provided invoice image and extract the following details:"""
full_prompt = f"{system_prompt}\nUser query: {input}"
if submit_button:
    try:
        image_part = input_image_details(uploaded_file)
        response=get_gemini_response(full_prompt,image_part)
        st.subheader("The extracted information is:")
        st.write(response)
 
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")    
    