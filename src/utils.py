# src/utils.py
"""
Module to handle the generation of chatbot responses using the Gemini API and ChromaDB.

This module contains functions that interact with the Gemini client to generate 
responses for the chatbot. The `create_completions` function builds a prompt 
using a user’s query and previous interactions, then sends it to the 
Gemini model to obtain a relevant response.

Functions:
    create_completions(client, query, interaction): Generates a completion from 
        the Gemini model based on the user's query and prior interactions.
    create_response(client, query, interaction): Generates a response from the Gemini model.
    respuesta_general(texto): Returns a general response.
"""

from prompt import build_prompt,build_prompt_recomendation,build_prompt_explain,build_prompt_comparation
from config import init_client


def create_completions(client, query, interaction):
    """
    Generates a chatbot completion based on the user's query and previous interactions.

    Args:
        client: GeminiClient instance used to generate content.
        query (str): The user's query.
        interaction (str): Previous interaction history.

    Returns:
        tuple: (output (str), action (str)) where output is the model's response and action is the detected action.
    """
    # Build the prompt
    prompt_text = build_prompt(query,interaction)

    # Generate the response
    response = client.generate_content(prompt_text, generation_config={"temperature": 0.5})

    # Extract and return the tex

    return response.candidates[0].content.parts[0].text.strip('`\n')

def analyze_product_details(client, query, product_details,name):
    """
    Analyzes product details and generates a response based on the user's query.

    Args:
        client: GeminiClient instance used to generate content.
        query (str): The user's query.
        product_details (dict): The product details to analyze.

    Returns:
        str: The generated response based on the analysis of the product details.
    """
    # Build the prompt
    prompt_text = build_prompt_explain(query, product_details,name)

    # Generate the response
    response = client.generate_content(prompt_text, generation_config={"temperature": 0.5})

    # Extract and return the text
    return response.candidates[0].content.parts[0].text.strip('`\n')

def compare_products(client, query, context):
    """
    Analyzes product details and generates a response based on the user's query.

    Args:
        client: GeminiClient instance used to generate content.
        query (str): The user's query.
        product_details (dict): The product details to analyze.

    Returns:
        str: The generated response based on the analysis of the product details.
    """
    # Build the prompt
    prompt_text = build_prompt_comparation(query, context)

    # Generate the response
    response = client.generate_content(prompt_text, generation_config={"temperature": 0.5})

    # Extract and return the text
    return response.candidates[0].content.parts[0].text.strip('`\n')

def create_crecomendation(client, query, products):
    """
    Generates a chatbot completion based on the user's query and previous interactions.

    Args:
        client: GeminiClient instance used to generate content.
        query (str): The user's query.
        interaction (str): Previous interaction history.

    Returns:
        tuple: (output (str), action (str)) where output is the model's response and action is the detected action.
    """
    # Build the prompt
    prompt_text = build_prompt_recomendation(query,products)

    # Generate the response
    response = client.generate_content(prompt_text, generation_config={"temperature": 0.5})

    # Extract and return the tex

    return response.candidates[0].content.parts[0].text.strip('`\n')
