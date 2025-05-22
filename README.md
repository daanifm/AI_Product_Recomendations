# 🛍️ Amazon AI Product Recommender & Analyzer

## Descripción

Este proyecto presenta un **sistema avanzado de recomendación y análisis de productos de Amazon**, impulsado por una arquitectura de **agentes de inteligencia artificial** y **web scraping dinámico**. La aplicación, construida con **Gradio** para una interfaz intuitiva, permite a los usuarios interactuar con la plataforma de tres maneras principales: realizar búsquedas generales de productos, profundizar en el análisis de artículos específicos y comparar productos lado a lado.

El corazón del sistema reside en sus agentes de IA especializados: un **agente discriminador** que dirige la interacción inicial, y agentes dedicados al web scraping y al análisis profundo de datos, garantizando una experiencia de usuario fluida y rica en información.

---

## Características Principales

* **🔍 Búsqueda General de Productos (Web Scraping General):**
    * Un **agente discriminador** inteligente decide si la consulta del usuario requiere una búsqueda amplia, activando un proceso de web scraping general sobre Amazon para obtener listados de productos relevantes.
    * Ideal para explorar una categoría o buscar ideas sin un producto específico en mente.

* **🔬 Análisis Profundo de Productos (Web Scraping Profundo & Análisis IA):**
    * Permite a los usuarios seleccionar productos obtenidos previamente (o introducir URLs específicas) para un **análisis detallado**.
    * Un agente especializado realiza un **web scraping profundo** para extraer toda la información disponible: descripciones, especificaciones técnicas, reseñas, preguntas y respuestas, y más.
    * Posteriormente, un agente de IA procesa y analiza esta información, resumiendo puntos clave, pros y contras, y extrayendo insights relevantes para el usuario.

* **⚖️ Comparación de Productos:**
    * Facilita la **comparación lado a lado** de múltiples productos, destacando similitudes y diferencias clave.
    * Utiliza los datos recopilados y analizados para ofrecer una visión clara que ayuda a los usuarios a tomar decisiones informadas.

---

## Arquitectura del Proyecto

El sistema se basa en una arquitectura de agentes de IA comunicativos, orquestados para manejar diferentes etapas del flujo de usuario:

* **Agente Discriminador:** Actúa como el punto de entrada, interpretando la intención del usuario para derivar la solicitud a la funcionalidad adecuada (búsqueda general, análisis profundo o comparación).
* **Agentes de Web Scraping:** Encargados de interactuar con Amazon, extrayendo datos de forma eficiente y robusta, tanto para búsquedas generales como para análisis detallados.
* **Agentes de Análisis de IA:** Procesan y contextualizan los datos extraídos, generando resúmenes, extrayendo características clave y preparando la información para la visualización o comparación.

---

## Tecnologías Utilizadas

* **Lenguaje de Programación:** Python
* **Interfaz de Usuario:** Gradio
* **Web Scraping:** `BeautifulSoup`
* **Agentes de IA:** Google **Gemini API (con Gemini 2.0 Flash)**

---

## Instalación y Uso

### Requisitos

* VSCode
* Python 3.12
* API Gemini
* BeautifulSoup
* Gradio

### Clonar el Repositorio

```bash
git clone [[https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)](https://github.com/daanifm/AI_Product_Recomendations.git)
cd tu-repositorio
