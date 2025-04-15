# mcp-vademecum

`mcp-vademecum` es un servidor MCP (Model Context Protocol) que permite la integración de información sobre medicamentos provenientes de la API de Vademécum de UMASalud para Argentina. Este servidor facilita la consulta y recuperación de datos sobre medicamentos, incluyendo detalles como la droga, presentación, dosis, laboratorio, y más.

## Descripción

El servidor expone una herramienta MCP llamada `buscar_medicamento`, que recibe una consulta de texto con el nombre de un medicamento y devuelve un listado de hasta 20 medicamentos encontrados, formateados para su uso en flujos de trabajo automáticos, integrables en sistemas de agentes de IA o modelos de lenguaje (LLMs).

### Función `buscar_medicamento`

Esta función se conecta a un endpoint de la API de Vademécum de UMASalud para Argentina, procesa la respuesta JSON y filtra los datos relevantes para integrarlos en flujos automatizados.

#### Parámetros:
- **query (str):** Nombre del medicamento o droga que se busca.

#### Retorna:
- **str:** Un texto que lista hasta 20 medicamentos encontrados, donde cada medicamento se presenta con:
  - **Nombre del producto** (resaltado en negrita)
  - Droga
  - Dosis
  - Presentación
  - Acción farmacológica
  - Laboratorio
  - alfabetRegisterNum (etiquetado como información para uso interno, no mostrado al usuario)

#### Ejemplo de salida:

1. **Ibuprofeno 400mg**
   - **Droga:** Ibuprofeno
   - **Dosis:** 400mg
   - **Presentación:** Tableta
   - **Acción farmacológica:** Antiinflamatorio y analgésico
   - **Laboratorio:** Laboratorio XYZ
   - **alfabetRegisterNum:** 123456 _(uso interno, no mostrar al usuario)_

2. **Paracetamol 500mg**
   - **Droga:** Paracetamol
   - **Dosis:** 500mg
   - **Presentación:** Tableta
   - **Acción farmacológica:** Analgésico y antipirético
   - **Laboratorio:** Laboratorio ABC
   - **alfabetRegisterNum:** 654321 _(uso interno, no mostrar al usuario)_


#### Excepciones:
- Si la URL de la API no está definida o hay errores de conexión, se lanza un `ValueError`.
- Si la respuesta del servidor contiene un JSON malformado, se lanza un `ValueError`.

#### Integración con MCP:
- Esta herramienta está adaptada al Model Context Protocol y puede ser invocada de forma estandarizada por agentes de IA.
- El formato de salida está diseñado para proveer contexto estructurado a modelos de lenguaje y facilitar su integración en flujos automatizados.

## Instalación

### Requisitos:
- Python 3.10 o superior
- Dependencias:
  - `fastmcp`
  - `requests`
  - `pydantic`

### Instalación desde PyPI

Puedes instalar el paquete directamente desde PyPI:

```bash
pip install mcp-vademecum
```

## Uso

### Ejecutar el Servidor

Para iniciar el servidor MCP, simplemente ejecuta:

```bash
mcp-vademecum
```

O bien, a través de Python:

```bash
python -m mcp_vademecum
```

## Ejemplo de Cliente MCP

Puedes conectarte a este servidor desde otro script usando el cliente MCP. Por ejemplo:

```python
from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport
import mcp_vademecum

async def main():
    async with Client(FastMCPTransport(mcp_vademecum.mcp)) as client:
        tools = await client.list_tools()
        print("Available tools:", tools)

        result = await client.call_tool("buscar_medicamento", {"query": "ibuprofeno"})
        print("Result:", result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```