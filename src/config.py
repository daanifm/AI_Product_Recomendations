
# src/config.py
"""
    Client to interact with the Google Gemini API using HTTP requests.
"""
import google.generativeai as genai
import os



def init_client():
    """
    Initializes the client to interact with the Google Gemini API.
    This function sets up the API key and configures the client for use.
    """
    # Initialize ChromaDB client

    api_key = os.getenv("API_KEY")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-2.0-flash')
    return model
