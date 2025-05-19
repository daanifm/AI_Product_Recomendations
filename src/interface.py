def get_html():
    return """
<style>
    body, html {
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, sans-serif;
        background-color: #AA9F9D !important;
        color: #111 !important;
    }

    .gradio-container {
        width: 100% !important;
        max-width: none !important;
        height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    #main_container {
        display: flex;
        flex-direction: column;
        height: 100vh;
        max-width: 800px;
        margin: 0 auto;
        background: #AA9F9D !important;
        border-radius: 16px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.07);
        overflow: hidden;
    }

    #chat_container {
        flex: 1;
        overflow-y: auto;
        padding: 20px 24px;
        background: #f8f9fa;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    #chatbot {
        padding: 0;
        min-height: 75vh;
        margin: 0;
    }

    .user, .bot {
        max-width: 120%;          /* Más ancho para mensajes largos */
        min-height: 40px;        /* Altura mínima para burbujas */
        padding: 14px 18px;
        font-size: 16px;         /* Un poco más grande para mejor lectura */
        line-height: 1.6;
        border-radius: 18px;
        background: #e9ecef;
        display: inline-block;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin-bottom: 10px;     /* Más espacio entre mensajes */
    }

    .user {
        align-self: flex-end;
        background: #007aff;
        color: white;
    }

    .bot {
        align-self: flex-start;
        background: #ececec;
        color: #111;
    }

    #input_container {
        padding: 12px 20px;
        background: white;
        border-top: 1px solid #e0e0e0;
        display: flex;
        justify-content: center;
        position: sticky;
        bottom: 0;
    }

    .input-wrapper {
        position: relative;
        width: 100%;
        max-width: 720px;
    }

    #query_input {
        width: 100%;
        padding: 14px 50px 14px 16px;
        border-radius: 24px;
        font-size: 15px;
        border: 1px solid #d0d0d0;
        background: #fefefe;
        outline: none;
    }

    #submit_button {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background-color: #007aff;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background-color 0.2s;
    }

    #submit_button:hover {
        background-color: #006ae6;
    }

    #chatbot::-webkit-scrollbar {
        width: 8px;
    }

    #chatbot::-webkit-scrollbar-track {
        background: transparent;
    }

    #chatbot::-webkit-scrollbar-thumb {
        background: #cccccc;
        border-radius: 4px;
    }

    @media (min-width: 1400px) {
        #main_container {
            max-width: 1000px;
        }
    }
</style>
"""
