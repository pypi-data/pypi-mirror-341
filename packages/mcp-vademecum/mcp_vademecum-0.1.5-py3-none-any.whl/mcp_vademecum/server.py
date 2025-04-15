import requests
from fastmcp import FastMCP
from typing import Annotated
from pydantic import Field
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP("vademecum")

@mcp.tool()
def buscar_medicamento(
    query: Annotated[str, Field(description="Nombre del medicamento o droga.")]
) -> str:
    """
    Busca información sobre medicamentos a partir de una consulta de texto y devuelve resultados formateados para su uso en flujos de trabajo MCP.

    Esta función se conecta al endpoint del Vademécum de UMASalud para Argentina (AR) utilizando la API especificada en la variable de entorno. Envía la consulta (query) mediante una solicitud HTTP POST, procesa la respuesta JSON y limita los resultados a los primeros 20. Los datos relevantes de cada medicamento (acción farmacológica, nombre del producto, droga, presentación, dosis, laboratorio y número de registro interno) se filtran y formatean en un texto estructurado, preparado para que un LLM o agente MCP lo integre en un flujo de contexto.

    Parámetros:
        query (str): Texto de la consulta para buscar información sobre medicamentos.

    Retorna:
        str: Un string formateado que enumera hasta 20 medicamentos encontrados con sus detalles, donde cada medicamento se presenta con:
             - Nombre del producto (resaltado en negrita)
             - Droga
             - Dosis
             - Presentación
             - Acción farmacológica
             - Laboratorio
             - alfabetRegisterNum (etiquetado como información para uso interno, no mostrada al usuario final)
             Si no se encuentran resultados, la función devuelve el mensaje "No se encontraron resultados."

    Excepciones:
        ValueError: Se lanza si la URL del API no está definida en el entorno, si ocurre un error en la conexión o solicitud HTTP,
                    o si la respuesta del servidor contiene un JSON malformado.

    Ejemplo de uso:
        >>> resultado = buscar_medicamento("ibuprofeno")
        >>> print(resultado)
        1. **Ibuprofeno 400mg**
           - Droga: Ibuprofeno
           - Dosis: 400mg
           - Presentación: Tableta
           - Acción farmacológica: Antiinflamatorio y analgésico
           - Laboratorio: Laboratorio XYZ
           - alfabetRegisterNum: 123456 _(uso interno, no mostrar al usuario)_

    Notas de integración con MCP:
        - Esta herramienta está adaptada al Model Context Protocol y puede ser invocada de forma estandarizada por agentes AI.
        - El formato de salida está diseñado para proveer contexto estructurado a modelos de lenguaje, permitiendo interpretar y utilizar la información en flujos automatizados.
    """
    url = os.getenv("API_VADEMECUM_URL")
    if not url:
        raise ValueError("API_VADEMECUM_URL no está definida en el entorno.")
    
    try:
        response = requests.post(
            url,
            json={"text": query, "country": "AR"},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        results = response.json().get('output', [])[:20]  # hasta 20 por si querés limitar después
        if not results:
            return "No se encontraron resultados."
        
        # Filtramos y estructuramos
        filtered_results = [
            {
                'Acción farmacológica': item['accion_farmacologica'],
                'Nombre del producto': item['productName'],
                'Droga': item['drugName'],
                'Presentación': item['presentationName'],
                'Dosis': item['dosis'],
                'Laboratorio': item['laboratorio'],
                'alfabetRegisterNum': item['alfabetRegisterNum']
            }
            for item in results
        ]

        # Formato estructurado para LLM
        result_strings = []
        for idx, item in enumerate(filtered_results, 1):
            formatted = (
                f"{idx}. **{item['Nombre del producto']}**\n"
                f"   - Droga: {item['Droga']}\n"
                f"   - Dosis: {item['Dosis']}\n"
                f"   - Presentación: {item['Presentación']}\n"
                f"   - Acción farmacológica: {item['Acción farmacológica']}\n"
                f"   - Laboratorio: {item['Laboratorio']}\n"
                f"   - alfabetRegisterNum: {item['alfabetRegisterNum']} _(uso interno, no mostrar al usuario)_"
            )
            result_strings.append(formatted)
        
        return "\n\n".join(result_strings)

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error de red o conexión: {e}")
    except ValueError:
        raise ValueError("Error en la respuesta del servidor: JSON malformado.")