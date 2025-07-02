# src/app.py
"""
This module defines the chatbot interface using Gradio, handles user interactions,
and manages the conversation history.

Functions:
    chatbot_interface(query, history, client, collection): Handles user input, fetches the response from the chatbot, and updates the conversation history.
    launch_gradio_interface(client, collection): Sets up and launches the Gradio interface for the chatbot, defining the UI components and connecting them to the chatbot logic.

Dependencies:
    - gradio
    - utils (create_completions, guardar_info, consulta_rag, respuesta_general)
    - config (init_client)
    - interface (get_html)
    - functools (partial)
"""

import gradio as gr
from utils import create_completions,create_crecomendation,analyze_product_details,compare_products
from config import init_client
from interface import get_html
from functools import partial
from scrapping import search_amazon_from_json,get_product_details_from_url
import json
# Define the interaction history as an empty list
interaccion = []  # Global interaction history

def chatbot_interface(query, history, client):
    """
    Handles user input, gets the response from the chatbot, and updates the conversation history.

    Args:
        query (str): The user's query input.
        history (list): The current conversation history.
        client: GeminiClient instance used to generate content.
        collection: ChromaDB collection instance.

    Returns:
        tuple: (history, history) - The updated conversation history for display and state.
    """
    global interaccion  # Use the global interaction history
    # Get the response and action from the chatbot
    response = create_completions(client, query, interaccion)

    if response.startswith("busqueda_detallada,"):
        try:
            response = response[len("jbusqueda_detallada,"):]
            if response.startswith("```json\n"):
                cleaned_response = response[len("```json\n"):]
            else:
                cleaned_response = response.strip()

            detailed_product_info = json.loads(cleaned_response)
            if "url" in detailed_product_info:
                detailed_info = get_product_details_from_url(detailed_product_info["url"])
                analysis = analyze_product_details(client, query, detailed_info,detailed_product_info["nombre"])
                final_response = f"Información detallada sobre '{detailed_product_info.get('nombre', 'este artículo')}':\n\n{analysis}"
            else:
                final_response = "No se pudo obtener la URL del artículo para la búsqueda detallada."
        except json.JSONDecodeError:
            final_response = "El modelo no devolvió un JSON válido para la búsqueda detallada."
        except ValueError:
            final_response = "El modelo indicó búsqueda detallada pero no proporcionó información del artículo."
        except Exception as e:
            final_response = f"Ocurrió un error al procesar la búsqueda detallada: {e}"
    elif response.startswith("comparacion,"):
        response = response[len("comparacion,"):]
        final_response = compare_products(client, response,interaccion)
    elif response.startswith("error,"):
        final_response = response[len("error,"):]
    else:
        try:
            # Limpiar el prefijo "json\n" si está presente
            if response.startswith("json\n"):
                cleaned_response = response[len("json\n"):]
            else:
                cleaned_response = response.strip()

            # Intentar decodificar la respuesta limpia como JSON
            json_response = json.loads(cleaned_response)
            products = search_amazon_from_json(json_response)
            final_response = create_crecomendation(client, query, products)

        except json.JSONDecodeError as e:
            products = f"No se pudieron buscar productos en este momento. Por favor, intenta de nuevo con una consulta más específica. Error: {e}"
            print(f"Error de decodificación JSON: {e}, Respuesta original: '{response}'")
    history.append((query, final_response))
    interaccion.append((query, final_response))
    return history, history
def launch_gradio_interface(client):
    chatbot_css = get_html()
    
    with gr.Blocks(title="My Custom Chatbot") as demo:
        gr.HTML(chatbot_css)
        gr.Markdown("# 🤖 AI Product Recommendations", elem_id="header")
        chatbot = gr.Chatbot(elem_id="chatbot",type="messages")
        
        with gr.Row(elem_id="input_container"):
            with gr.Column(elem_classes=["input-wrapper"]):
                query_input = gr.Textbox(
                    placeholder="Type your message here...",
                    show_label=False,
                    elem_id="query_input"
                )
                submit_button = gr.Button("➤", elem_id="submit_button")
        
        chatbot_interface_with_client = partial(chatbot_interface, client=client)

        submit_button.click(
            chatbot_interface_with_client,
            inputs=[query_input, chatbot],
            outputs=[chatbot, chatbot]
        )
        query_input.submit(
            chatbot_interface_with_client,
            inputs=[query_input, chatbot],
            outputs=[chatbot, chatbot]
        )
    
    demo.launch(server_name="0.0.0.0", server_port=7860)
