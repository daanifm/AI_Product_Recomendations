import requests
from bs4 import BeautifulSoup


def get_product_details_from_url(url: str) -> str:
    """
    Extracts all visible text from an Amazon product page for further analysis with an LLM.

    Args:
        url (str): URL of the Amazon product.

    Returns:
        str: Complete visible text from the page or an error message.
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/114.0.0.0 Safari/537.36'
        ),
        'Accept-Language': 'es-ES,es;q=0.9'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Elimina scripts y estilos
        for element in soup(['script', 'style', 'noscript', 'header', 'footer', 'svg']):
            element.decompose()

        # Extrae texto visible
        text = soup.get_text(separator='\n')
        lines = [line.strip() for line in text.splitlines()]
        visible_text = '\n'.join(line for line in lines if line)

        if not visible_text.strip():
            return "No se pudo extraer texto visible de la página."

        return visible_text.strip()

    except requests.exceptions.RequestException as e:
        return f"Error al acceder a la URL del producto: {e}"
    except Exception as e:
        return f"Ocurrió un error al procesar la página: {e}"
    
def search_amazon_from_json(json_data):
    """
    Searches for products on Amazon based on the provided JSON data.

    Args:
        json_data (dict): A dictionary containing product details (e.g., name, brand, price range).

    Returns:
        list: A list of dictionaries, where each dictionary represents a product found on Amazon
              and includes its title, price, and URL. Returns an empty list if no products are found
              or if an error occurs.
    """
    base_url = "https://www.amazon.es/s?"
    query_params = {}
    if "nombre" in json_data and json_data["nombre"]:
        query_params["k"] = json_data["nombre"]

    if "marca" in json_data and json_data["marca"]:
        if "k" in query_params:
            query_params["k"] += " " + json_data["marca"]
        else:
            query_params["k"] = json_data["marca"]

    if "precio_min" in json_data and json_data["precio_min"] is not None:
        query_params["low-price"] = str(json_data["precio_min"])
    if "precio_max" in json_data and json_data["precio_max"] is not None:
        query_params["high-price"] = str(json_data["precio_max"])
    if "sexo" in json_data and json_data["sexo"]:
        if "k" in query_params:
            query_params["k"] += " " + json_data["sexo"]
        else:
            query_params["k"] = json_data["sexo"]
    if "caracteristicas" in json_data and json_data["caracteristicas"]:
        for feature in json_data["caracteristicas"]:
            if "k" in query_params:
                query_params["k"] += " " + feature
            else:
                query_params["k"] = feature

    # Construct the URL
    url = base_url + "&".join([f"{key}={value}" for key, value in query_params.items()])

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        productos = []
        # Update the selector to match the current Amazon page structure.
        # This selector might need to be adjusted frequently.
        titulos_productos = soup.find_all('h2', class_='a-size-base-plus a-spacing-none a-color-base a-text-normal')

        for titulo_elemento in titulos_productos[:5]:  # Limit to the first 5 results
            titulo_span = titulo_elemento.find('span')
            if titulo_span:
                titulo = titulo_span.text.strip()
                # Find the parent element that contains both title and price
                product_div = titulo_elemento.find_parent('div', {'data-component-type': 's-search-result'})
                if product_div:
                    # Extract price
                    price_whole_element = product_div.find('span', class_='a-price-whole')
                    price_fraction_element = product_div.find('span', class_='a-price-fraction')
                    if price_whole_element and price_fraction_element:
                        precio = float(price_whole_element.text.strip().replace(',', '') + '.' + price_fraction_element.text.strip())
                    else:
                        precio = "Precio no disponible"
                    # Extract product URL
                    enlace_elemento = product_div.find('a', class_='a-link-normal', href=True)
                    if enlace_elemento:
                        producto_url = 'https://www.amazon.es' + enlace_elemento['href']
                    else:
                        producto_url = "URL no disponible"

                    productos.append({'titulo': titulo, 'precio': precio, 'producto_url': producto_url})
        return productos

    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return []
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []
    
    