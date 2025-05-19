# src/main.py
"""
This module initializes the client and launches the Gradio interface for the chatbot.

The primary function of this module is to set up the necessary components and 
start the Gradio interface where users can interact with the chatbot.

Modules:
- `init_client`: Initializes the client used to interact with the chatbot model.
- `launch_gradio_interface`: Sets up and runs the Gradio interface 
for user interaction with the chatbot.

This module does not contain any additional business logic but serves as an entry 
point to start the chatbot system.
"""

from config import init_client
from app import launch_gradio_interface

# Initialize the client
client = init_client()

# Launch the Gradio interface
launch_gradio_interface(client)
