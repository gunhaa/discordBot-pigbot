import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def supervive():
    
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    result = model.generate_content()
   
    
    return