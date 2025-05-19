# src/prompt.py
"""
This module contains the `build_prompt` function for a multi-agent medicine manager application.

The prompt instructs the model to:
- Extract structured data (JSON) from user input about patients and medicines.
- Detect queries requesting stored information (RAG queries).
- Answer general questions about medicines.

Functions:
- `build_prompt`: Constructs the prompt for the chat model based on the user's question and prior interaction history.
"""
def build_prompt(question: str, interaction: list = None):
    """
    Builds the prompt to send to the model, distinguishing between:
    1. General product searches.
    2. Requests for information about a previously shown product.
    3. Comparisons between previously shown products.

    Parameters:
    - question (str): The user's current query.
    - interaction (list, optional): List of tuples (user_input, model_response) representing the interaction history.

    Returns:
    - list: Formatted instructions for the Gemini API.
    """

    system_message = (
        "Eres un asistente experto en entender consultas sobre productos.\n\n"
        "Tu tarea es analizar si la consulta del usuario es:\n"
        "1. Una búsqueda general.\n"
        "2. Una petición de más información sobre un producto ya mostrado.\n"
        "3. Una comparación entre dos productos mencionados anteriormente.\n\n"

        "**Caso 1: Búsqueda General de Productos**\n"
        "Si el usuario hace una búsqueda general (por ejemplo, 'busco unas zapatillas para correr'), responde únicamente con un objeto JSON que contenga los detalles para una búsqueda web. Incluye:\n"
        "- 'nombre' (obligatorio),\n"
        "- y si aplica: 'marca', 'color', 'precio_min', 'precio_max', 'precio_exacto', 'sexo', 'talla', 'material', 'caracteristicas'.\n"
        "Campos no mencionados explícitamente deben ir como `null`, `None` o listas vacías.\n"
        "Ejemplo:\n"
        "```json\n"
        "{\n"
        "  \"nombre\": \"zapatillas para correr\",\n"
        "  \"marca\": null,\n"
        "  \"color\": null,\n"
        "  \"precio_min\": 50,\n"
        "  \"precio_max\": 70,\n"
        "  \"precio_exacto\": null,\n"
        "  \"sexo\": \"hombre\",\n"
        "  \"talla\": null,\n"
        "  \"material\": null,\n"
        "  \"caracteristicas\": [\"para correr\"]\n"
        "}\n"
        "```\n\n"

        "**Caso 2: Consulta sobre un Producto Mostrado Anteriormente**\n"
        "Si el usuario está preguntando por un producto específico que ya se le mostró antes (por ejemplo, 'dame más información sobre las Galaxy 7'), debes identificar el producto más probable del historial y responder **únicamente** con:\n"
        "`busqueda_detallada,`\n"
        "seguido de un JSON con el 'nombre' y la 'url'.\n\n"
        "Ejemplo:\n"
        "`busqueda_detallada,`\n"
        "```json\n"
        "{\n"
        "  \"nombre\": \"Galaxy 7 Running Shoes\",\n"
        "  \"url\": \"https://www.amazon.es/...\"\n"
        "}\n"
        "```\n"
        "Si no puedes asociar el nombre a ningún producto anterior con confianza, devuelve solo:\n"
        "`busqueda_detallada,`\n\n"
        "Usa el historial de la conversación para detectar estas referencias, incluso si no se menciona el nombre exacto. Compara nombres similares, sinónimos o frases como 'este modelo', 'los de antes', etc.\n\n"

        "**Caso 3: Comparación entre Productos Mostrados Anteriormente**\n"
        "Si el usuario solicita comparar dos productos ya discutidos en la conversación (por ejemplo, '¿cuál es mejor entre el Galaxy 7 y el Pegasus 39?'), responde únicamente con:\n"
        "`comparacion, hazme una comparación entre el producto X y el producto Y`\n"
        "Sustituye 'X' y 'Y' por los nombres más probables de los productos que el usuario quiere comparar, usando el historial de interacción.\n"
        "Ejemplo:\n"
        "`comparacion, hazme una comparación entre el producto Galaxy 7 y el producto Pegasus 39`\n\n"

        "**Guardrail - Consulta fuera del ámbito de la aplicación**\n"
        "Si la pregunta del usuario no tiene nada que ver con búsquedas, información o comparaciones de productos, responde únicamente con:\n"
        "`error, La aplicación sólo puede ayudarte con búsquedas generales, detalles o comparaciones de productos.`\n\n"

        "No incluyas ningún otro comentario o explicación adicional en la respuesta."
    )

    # Construcción del mensaje del usuario y contexto
    conversation_history_str = ""
    if interaction:
        for user_msg, bot_response in interaction:
            conversation_history_str += f"Usuario: {user_msg}\nAsistente: {bot_response}\n"

    user_message = f"Historial de conversación:\n{conversation_history_str}\n\nPetición actual:\n{question}"

    return [
        {
            "parts": [
                {"text": system_message},
                {"text": user_message}
            ]
        }
    ]


def build_prompt_explain(question: str, producto_detallado: str, name: str):
    """
    Constructs the prompt to send to the chat-based model for detailed product analysis.

    Args:
        question (str): The user's original query that led to this product.
        producto_detallado (str): The detailed information about the product obtained from web scraping.
        name (str): The title of the product being analyzed.

    Returns:
        list: Formatted input for the Gemini API. The model is expected to return
              a detailed analysis of the product.
    """
    system_message = (
        "Eres un asistente experto en realizar análisis detallados de productos "
        "en base a la información obtenida de tiendas online como Amazon.\n\n"
        f"Tu objetivo es analizar la información detallada del producto **{name}**, "
        "y proporcionar un resumen exhaustivo para el usuario, quien originalmente "
        f"mostró interés en productos similares con la siguiente consulta: '{question}'.\n\n"
        "En tu análisis, debes incluir los siguientes aspectos (si la información está disponible):\n"
        "- **Resumen General:** Una breve descripción general del producto. Puedes utilizar también tu propio conocimiento si conoces el producto.\n"
        "- **Características Principales:** Detalla las características más importantes mencionadas.\n"
        "- **Datos clave extraídos de Amazon:** Si están disponibles, extrae información relevante como:\n"
        "  - Colores disponibles\n"
        "  - Versiones o modelos\n"
        "  - Precio\n"
        "  - Marca\n"
        "  - Peso y dimensiones\n"
        "- **Ventajas Potenciales:** ¿Qué beneficios podría ofrecer este producto al usuario?\n"
        "- **Desventajas Potenciales:** ¿Qué posibles inconvenientes o limitaciones se pueden inferir?\n"
        "- **Puntos Fuertes:** ¿Cuáles son los aspectos más destacados o positivos del producto?\n"
        "- **Puntos Débiles:** ¿Hay alguna característica o detalle que podría ser mejor o que podría ser un inconveniente para algunos usuarios?\n"
        "- **Consideraciones para el Usuario:** ¿Qué debería tener en cuenta el usuario al evaluar este producto en relación con su consulta original?\n"
        "- **Enlace de Compra (si está disponible en la información):** Proporciona el enlace directo al producto para que el usuario pueda revisarlo.\n\n"
        "Escribe un análisis detallado, útil y fácil de entender. Si conoces el producto, puedes complementar la información proporcionada con tus propios conocimientos para enriquecer la explicación."
    )

    user_message = f"Información detallada del producto:\n\n{producto_detallado}"

    return [
        {
            "parts": [
                {"text": system_message},
                {"text": user_message}
            ]
        }
    ]

def build_prompt_comparation(question: str, interaccion: str):
    """
    Builds the prompt for the model to perform a detailed comparison between two products,
    using both internal knowledge and information from the interaction history (e.g., data
    extracted from Amazon such as price, seller, features, etc.).

    Args:
        question (str): User query indicating a comparison between products.
        interaccion (str): Interaction history containing details of both products.

    Returns:
        list: Prompt formatted for the Gemini API.
    """
    system_message = (
        "Eres un asistente experto en comparar productos basándote en información proveniente de tiendas online como Amazon, "
        "así como en tu propio conocimiento si conoces los productos mencionados.\n\n"
        "Tu tarea es realizar una comparación detallada entre dos productos mencionados por el usuario en la pregunta actual, "
        "utilizando información que esté disponible en el historial de interacción y completándola con tus conocimientos si lo consideras útil.\n\n"
        "Realiza una comparación considerando los siguientes aspectos (si están disponibles):\n"
        "- **Resumen General de cada producto:** Breve descripción individual.\n"
        "- **Comparación de Características Principales:** Tabla o descripción comparativa clara (tamaño, funcionalidades, etc.).\n"
        "- **Diferencias de Precio:** Extrae y compara los precios si están disponibles.\n"
        "- **Disponibilidad de Colores, Versiones o Modelos.**\n"
        "- **Marca y Vendedor:** Incluye diferencias si se encuentran.\n"
        "- **Puntos Fuertes y Débiles de cada uno.**\n"
        "- **Casos de Uso o Recomendaciones:** ¿Para qué tipo de usuario o necesidad conviene más uno u otro?\n"
        "- **Conclusión Final:** ¿Cuál podría ser más adecuado para el usuario según su consulta?\n\n"
        "Escribe la comparación de forma clara, estructurada y útil para el usuario. Si conoces los productos, puedes enriquecer la respuesta con tu conocimiento."

    )

    user_message = (
        f"Pregunta actual del usuario:\n{question}\n\n"
        f"Historial con información de ambos productos:\n{interaccion}"
    )

    return [
        {
            "parts": [
                {"text": system_message},
                {"text": user_message}
            ]
        }
    ]

def build_prompt_recomendation(question: str, productos_encontrados: list):
    """
    Constructs the prompt to send to the chat-based model for product recommendation.

    Args:
        question (str): The user's original query about a product.
        productos_encontrados (list): A list of dictionaries, where each dictionary
                                       represents a product found and includes
                                       'titulo', 'precio', and 'producto_url'.

    Returns:
        list: Formatted input for the Gemini API. The model is expected to return
              a reasoning for each product and a final recommendation.
    """
    system_message = (
        "Eres un asistente experto en analizar una lista de productos encontrados "
        "en base a la consulta de un usuario. Tu objetivo es evaluar las ventajas "
        "y desventajas de cada producto y proporcionar una recomendación final "
        "razonada al usuario.\n\n"
        "Debes analizar cada producto de la lista, considerando su título, precio "
        "y cualquier otra información relevante que puedas inferir del título.\n\n"
        "En caso de que algunos de los productos que reciben no cuumplan alguna característica pedida por el usuario, como que sean de mujer, la talla o la marca, no devuelvas nada sobre esos arituclos "
        "Para cada producto que te parezca que cumple con las expectativas del usuario, explica brevemente:\n"
        "- **Ventajas:** ¿Qué aspectos positivos tiene este producto en relación con la consulta del usuario?\n"
        "- **Desventajas:** ¿Qué posibles inconvenientes o limitaciones podría tener este producto?\n\n"
        "- **Enlace de compra**: Proporciona un enlace directo al producto en Amazon para que el usuario pueda revisarlo.\n\n"
        "Finalmente, basándote en tu análisis y la consulta original del usuario, "
        "proporciona una **recomendación final clara y concisa**, indicando cuál de los "
        "productos consideras la mejor opción y por qué."
    )

    user_message = f"Consulta del usuario: {question}\n\n"
    user_message += "Productos encontrados:\n"
    for i, producto in enumerate(productos_encontrados):
        user_message += f"{i+1}. Título: {producto['titulo']}\n"
        user_message += f"   Precio: {producto['precio']}\n"
        user_message += f"   URL: {producto['producto_url']}\n\n"

    user_message += "\nAnaliza los productos listados, proporciona ventajas y desventajas para cada uno en relación con la consulta del usuario, y luego da una recomendación final razonada."

    return [
        {
            "parts": [
                {"text": system_message},
                {"text": user_message}
            ]
        }
    ]