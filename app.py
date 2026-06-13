from dotenv import load_dotenv
import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
# from typer import prompt
load_dotenv()
# Create two columns: left for title, right for name/date


    
# Sidebar input for API key

#Initialize our Streamlit app
st.set_page_config(page_title="AI Invoice Extractor", page_icon=":money_with_wings:")
st.title("AI Invoice Extractor")

st.header("Extract text from invoice images")
input=st.text_input("Enter your query about the invoice (e.g., 'What is the total amount?')","", key="input")
uploaded_file = st.file_uploader("Upload an invoice image", type=["jpg", "jpeg", "png"])    
submit_button = st.button("Tell me about the invoice")


api_key = st.sidebar.text_input("Enter your GEMINI_API_KEY ","81", placeholder="Enter your GEMINI_API_KEY ",type="password")
st.sidebar.markdown(f"Model used: **{os.getenv('Model')}**")

st.sidebar.markdown( "<span style='color:red; font-size:14px; font-weight:bold;'>ErShubhamBhagat</span>",
        unsafe_allow_html=True)
st.sidebar.markdown(
        f"<span style='color:red; font-size:12px;'>Developed on {os.getenv('constant_date')}</span>",
        unsafe_allow_html=True
    )    
    
    
if not api_key.strip():
    st.info("Please enter your GEMINI_API_KEY in the sidebar.")

# Gemini_API_KEY = os.getenv('GEMINI_API_KEY')
if(api_key==os.getenv('key')):
     Gemini_API_KEY = os.getenv('GEMINI_API_KEY')
else:
    Gemini_API_KEY = api_key

if not Gemini_API_KEY:
    raise ValueError("Gemini API key not found. ")

genai.configure(api_key=Gemini_API_KEY)
model = genai.GenerativeModel(os.getenv('Model'))

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
        st.spinner("The extracted information is:")
        st.write(response)
 
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")    
    