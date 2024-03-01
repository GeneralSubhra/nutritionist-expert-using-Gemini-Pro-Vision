import streamlit as st 
import google.generativeai as genai 
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text 

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
##making streamlit app app frontend
st.set_page_config(page_title="Calories Advisor App")
st.header("Calories Advisor App")
uploaded_file = st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uplaoded Image.",use_column_width=True)
    
submit=st.button("Tell me about the food")            

input_prompt ="""
You are an expert in nutritionist where you need to see the food items from the image and calculate the 
total calories and protein ,also provide the details of every food items with calories intake in table format 

columns name will be Item number,item name,calories,protein per 100grams ,carbs per 100 grams

Finally you can also mention whether the food is healthy or not and also mention the percentage split of the
ratio of carbohydrates,protein,fats,fibers,sugar and other nutritions required in our diet


"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.header("The response is: ")
    st.write(response)