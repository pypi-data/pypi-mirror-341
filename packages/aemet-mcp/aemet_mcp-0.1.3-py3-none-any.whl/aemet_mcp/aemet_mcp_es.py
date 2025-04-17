from typing import Any
import httpx
import json
from pathlib import Path
import logging
from mcp.server.fastmcp import FastMCP
#from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AemetMCPServer_es")

# Inicializar servidor FastMCP
mcp = FastMCP(
    "aemet-mcp-es",
    description="Servidor MCP para hacer consultas a la API de AEMET (Agencia Estatal de Meteorología de España). Para interactuar en español"
)

# Constantes
AEMET_API_BASE = "https://opendata.aemet.es/opendata/api"
# Obtener clave API desde https://opendata.aemet.es/centrodedescargas/altaUsuario?
API_KEY = os.getenv("AEMET_API_KEY", "ND")

# Cargar los códigos de playas al iniciar
with open(Path("../../res/Playas_codigos.json"), encoding="utf-8") as f:
    CODIGOS_PLAYAS = json.load(f)


# Diccionario para búsqueda exacta
NOMBRE_A_CODIGO = {
    playa["NOMBRE_PLAYA"].lower(): playa["ID_PLAYA"] for playa in CODIGOS_PLAYAS
}
# Diccionario de provincias → lista de playas
PROVINCIA_A_PLAYAS = {}
for playa in CODIGOS_PLAYAS:
    provincia = playa["NOMBRE_PROVINCIA"].lower()
    PROVINCIA_A_PLAYAS.setdefault(provincia, []).append(playa)


async def make_aemet_request(url: str) -> dict[str, Any] | None:
    """Realizar una petición a la API de AEMET con manejo adecuado de errores."""

    logger.info(f"make_aemet_request")

    headers = {
        "api_key": API_KEY,
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # La API de AEMET primero devuelve una URL de datos
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data_info = response.json()
            
            # Obtener los datos reales desde la URL proporcionada
            if data_info.get("estado") == 200:
                data_url = data_info.get("datos")
                if data_url:
                    data_response = await client.get(data_url, timeout=30.0)
                    data_response.raise_for_status()
                    # Manejar correctamente la codificación
                    content = data_response.content.decode('latin1')
                    return json.loads(content)
            return None
        except Exception as e:
            logger.error(f"Error al conectar con AEMET: {str(e)}")
            return None

def buscar_playas_por_nombre(nombre_parcial: str):
    nombre_parcial = nombre_parcial.lower()
    return [
        playa for playa in CODIGOS_PLAYAS
        if nombre_parcial in playa["NOMBRE_PLAYA"].lower()
        or playa["NOMBRE_PROVINCIA"].lower() in nombre_parcial
    ]


@mcp.tool()
async def pronostico_diario(municipality_code: str) -> str:
    """Obtener el pronóstico meteorológico diario para un municipio español.
    
    Args:
        municipality_code: Código de municipio AEMET (p.ej., "28079" para Madrid)
    """
    url = f"{AEMET_API_BASE}/prediccion/especifica/municipio/diaria/{municipality_code}"
    data = await make_aemet_request(url)
    
    if not data:
        return "No se pudieron obtener datos de pronóstico para este municipio."
    
    try:
        forecast = data[0]
        prediction = forecast.get("prediccion", {})
        day = prediction.get("dia", [])[0]
        
        result = f"""
Municipio: {forecast.get('nombre', 'Desconocido')}
Fecha: {day.get('fecha', 'Desconocida')}

Temperatura:
  Máxima: {day.get('temperatura', {}).get('maxima', 'N/D')}°C
  Mínima: {day.get('temperatura', {}).get('minima', 'N/D')}°C

Estado del Cielo: {day.get('estadoCielo', [{}])[0].get('descripcion', 'N/D')}
Probabilidad de Lluvia: {day.get('probPrecipitacion', [{}])[0].get('value', 'N/D')}%
Viento: {day.get('viento', [{}])[0].get('velocidad', 'N/D')} km/h {day.get('viento', [{}])[0].get('direccion', '')}
"""
        return result
    except Exception as e:
        return f"Error al procesar los datos del pronóstico: {str(e)}"

@mcp.tool()
async def datos_estacion(station_id: str) -> str:
    """Obtener datos meteorológicos específicos para una estación meteorológica.
    
    Args:
        station_id: Identificador de la estación (p.ej., "8416Y" para Valencia)
    """
    url = f"{AEMET_API_BASE}/observacion/convencional/datos/estacion/{station_id}"
    data = await make_aemet_request(url)
    
    if not data:
        return "No se pudieron obtener datos meteorológicos para esta estación."
    
    try:
        latest = data[0]
        result = f"""
Estación: {latest.get('ubi', 'Desconocida')}
Hora: {latest.get('fint', 'Desconocida')}

Temperatura: {latest.get('ta', 'N/D')}°C
Humedad: {latest.get('hr', 'N/D')}%
Velocidad del Viento: {latest.get('vv', 'N/D')} m/s
Dirección del Viento: {latest.get('dv', 'N/D')}°
Presión: {latest.get('pres', 'N/D')} hPa
Precipitación (1h): {latest.get('prec', 'N/D')} mm
"""
        return result
    except Exception as e:
        return f"Error al procesar los datos meteorológicos: {str(e)}"

@mcp.tool()
async def lista_estationes() -> str:
    """Obtener una lista de todas las estaciones meteorológicas disponibles."""
    url = f"{AEMET_API_BASE}/valores/climatologicos/inventarioestaciones/todasestaciones"
    data = await make_aemet_request(url)
    
    if not data:
        return "No se pudo obtener la lista de estaciones."
    
    try:
        stations = []
        for station in data:
            stations.append(f"ID: {station.get('indicativo', 'N/D')} - {station.get('nombre', 'Desconocido')} ({station.get('provincia', 'Desconocida')})")
        
        return "\n".join(stations)
    except Exception as e:
        return f"Error al procesar los datos de las estaciones: {str(e)}"

@mcp.tool()
async def datos_historicos(station_id: str, start_date: str, end_date: str) -> str:
    """Obtener datos históricos meteorológicos para una estación específica.
    
    Args:
        station_id: Identificador de la estación (p.ej., "3195" para Madrid Retiro)
        start_date: Fecha de inicio en formato AAAA-MM-DD
        end_date: Fecha de fin en formato AAAA-MM-DD
    """
    logger.info(f"start_date: ", start_date)

    # Formatear fechas para la API de AEMET (AAAA-MM-DDTHH:MM:SSUTC)
    start = start_date + "T00:00:00UTC"
    end = end_date + "T23:59:59UTC"
    
    url = f"{AEMET_API_BASE}/valores/climatologicos/diarios/datos/fechaini/{start}/fechafin/{end}/estacion/{station_id}"
    data = await make_aemet_request(url)
    
    if not data:
        return "No se pudieron obtener datos históricos para esta estación."
    
    try:
        result = []
        result.append(f"Datos Históricos para la Estación {station_id}")
        result.append(f"Período: {start_date} a {end_date}\n")
        
        for day in data:
            date = day.get('fecha', 'Fecha Desconocida')
            result.append(f"Fecha: {date}")
            result.append(f"Temperatura Máxima: {day.get('tmax', 'N/D')}°C")
            result.append(f"Temperatura Mínima: {day.get('tmin', 'N/D')}°C")
            result.append(f"Temperatura Media: {day.get('tmed', 'N/D')}°C")
            result.append(f"Precipitación: {day.get('prec', 'N/D')} mm")
            result.append(f"Velocidad del Viento: {day.get('velmedia', 'N/D')} km/h")
            result.append(f"Velocidad Máxima del Viento: {day.get('racha', 'N/D')} km/h")
            result.append(f"Horas de Sol: {day.get('sol', 'N/D')} horas")
            result.append("-" * 40 + "\n")
        
        return "\n".join(result)
    except Exception as e:
        return f"Error al procesar los datos históricos: {str(e)}"

@mcp.tool()
async def datos_climaticos_mensuales(estacion_id: str, anio: int, mes: int) -> str:
    """Obtiene el resumen climatológico mensual de una estación meteorológica.
    
    Args:
        estacion_id: Identificador de la estación (por ejemplo, "3195" para Madrid Retiro).
        anio: Año (formato YYYY).
        mes: Mes (1-12).
        
    Returns:
        Un texto con el resumen climático mensual o un mensaje de error si no hay datos disponibles.
    """
    mes_str = str(mes).zfill(2)
    url = f"{AEMET_API_BASE}/valores/climatologicos/mensualesanuales/datos/anioini/{anio}/aniofin/{anio}/estacion/{estacion_id}"
    data = await make_aemet_request(url)

    if not data:
        return "No se ha podido obtener el resumen climatológico mensual para esta estación."

    try:
        result = []
        registro = next((r for r in data if r.get("fecha", "").split("-")[-1] == mes_str), None)
        
        if not registro:
            return f"No hay datos disponibles para la estación {estacion_id} en {anio}-{mes_str}."

        result.append(f"Resumen Climatológico Mensual de la Estación {registro.get('nombre', estacion_id)} ({estacion_id})")
        result.append(f"Provincia: {registro.get('provincia', 'N/D')}")
        result.append(f"Altitud: {registro.get('altitud', 'N/D')} m")
        result.append(f"Año: {anio}, Mes: {mes}\n")

        # Temperatura
        result.append(f"Temperatura media de las máximas: {registro.get('tm_max', 'N/D')} °C")
        result.append(f"Temperatura media de las mínimas: {registro.get('tm_min', 'N/D')} °C")
        result.append(f"Temperatura media mensual: {registro.get('tm_mes', 'N/D')} °C")
        result.append(f"Temperatura máxima absoluta: {registro.get('ta_max', 'N/D')} °C")
        result.append(f"Temperatura mínima absoluta: {registro.get('ta_min', 'N/D')} °C")

        # Precipitación
        result.append(f"Precipitación total mensual: {registro.get('p_mes', 'N/D')} mm")
        result.append(f"Precipitación máxima diaria: {registro.get('p_max', 'N/D')}")
        result.append(f"Días de lluvia: {registro.get('n_llu', 'N/D')}")
        result.append(f"Días de nieve: {registro.get('n_nie', 'N/D')}")
        result.append(f"Días con tormenta: {registro.get('n_tor', 'N/D')}")
        result.append(f"Días con niebla: {registro.get('n_fog', 'N/D')}")

        # Humedad y radiación solar
        result.append(f"Humedad relativa media: {registro.get('hr', 'N/D')}%")
        result.append(f"Insolación media diaria: {registro.get('inso', 'N/D')} h")
        result.append(f"Porcentaje de insolación respecto al teórico: {registro.get('p_sol', 'N/D')}%")

        # Viento
        result.append(f"Racha máxima de viento: {registro.get('w_racha', 'N/D')}")
        result.append(f"Velocidad media del viento: {registro.get('w_med', 'N/D')} km/h")
        result.append(f"Días con viento ≥ 55 km/h: {registro.get('nw_55', 'N/D')}")
        result.append(f"Días con viento ≥ 91 km/h: {registro.get('nw_91', 'N/D')}")

        # Presión atmosférica
        result.append(f"Presión media en estación: {registro.get('q_med', 'N/D')} hPa")
        result.append(f"Presión máxima: {registro.get('q_max', 'N/D')} hPa")
        result.append(f"Presión mínima: {registro.get('q_min', 'N/D')} hPa")
        result.append(f"Presión media al nivel del mar: {registro.get('q_mar', 'N/D')} hPa")

        return "\n".join(result)

    except Exception as e:
        return f"Error procesando los datos climáticos mensuales: {str(e)}"

@mcp.tool()
def resolver_codigo_playa(nombre_o_codigo: str) -> str:
    """
    Resuelve el nombre y código exactos de una playa a partir de un nombre parcial o código.

    Args:
        nombre_o_codigo: Nombre de playa o código.

    Returns:
        Nombre correcto de la playa y su ID_PLAYA, o una lista de coincidencias/sugerencias.
    """
    entrada = nombre_o_codigo.strip().lower()

    # Si es un número, verificar si corresponde a un ID_PLAYA
    if entrada.isdigit():
        for playa in CODIGOS_PLAYAS:
            if str(playa["ID_PLAYA"]) == entrada:
                return (
                    f"Coincidencia exacta:\n"
                    f"Nombre: {playa['NOMBRE_PLAYA']}\n"
                    f"Código: {playa['ID_PLAYA']}\n"
                    f"Provincia: {playa['NOMBRE_PROVINCIA']}\n"
                    f"Municipio: {playa['NOMBRE_MUNICIPIO']}"
                )
        return f"No se encontró ninguna playa con el código {nombre_o_codigo}."

    # Buscar coincidencias por nombre parcial
    coincidencias = buscar_playas_por_nombre(entrada)

    if len(coincidencias) == 0:
        return f"No se encontraron playas que coincidan con '{nombre_o_codigo}'."

    if len(coincidencias) == 1:
        playa = coincidencias[0]
        return (
            f"Coincidencia exacta:\n"
            f"Nombre: {playa['NOMBRE_PLAYA']}\n"
            f"Código: {playa['ID_PLAYA']}\n"
            f"Provincia: {playa['NOMBRE_PROVINCIA']}\n"
            f"Municipio: {playa['NOMBRE_MUNICIPIO']}"
        )

    # Si hay varias coincidencias
    listado = "\n".join(
        f"- {p['NOMBRE_PLAYA']} (Código: {p['ID_PLAYA']}, {p['NOMBRE_PROVINCIA']})"
        for p in coincidencias
    )
    return (
        f"Se encontraron varias coincidencias para '{nombre_o_codigo}':\n"
        f"{listado}\nPor favor, especifica el nombre completo o el código exacto."
    )

@mcp.tool()
async def obtener_datos_playa_uv(nombre_o_codigo: str, dias_frc: int, tipo_consulta: str = "playa") -> str:
    """Consulta información sobre playas o índice UV desde AEMET.

    Args:
        nombre_o_codigo: Nombre parcial o completo de la playa, o su ID_PLAYA. También acepta 'listar' o 'listar:<provincia>'.
        dias_frc: Número de días para la previsión, desde 0, que significa 0 días a partir de hoy, hasta 4, quesignifica 4 días a partir de hoy.
        tipo_consulta: 'playa' para predicción, 'indice_uv' para índice UV. Los datos devueltos en el caso de índice UV son para todas las playas del país

    Returns:
        Información solicitada o lista de coincidencias.
    """
    comando = nombre_o_codigo.strip().lower()

    if comando == "listar":
        return "Playas disponibles:\n" + "\n".join(
            f"{p['NOMBRE_PLAYA']} ({p['NOMBRE_PROVINCIA']})"
            for p in sorted(CODIGOS_PLAYAS, key=lambda x: x["NOMBRE_PLAYA"])
        )

    if comando.startswith("listar:"):
        provincia = comando.split("listar:", 1)[1].strip()
        playas = PROVINCIA_A_PLAYAS.get(provincia.lower())
        if not playas:
            return f"No se encontraron playas para la provincia '{provincia}'."
        return f"Playas en {provincia.title()}:\n" + "\n".join(
            p["NOMBRE_PLAYA"] for p in sorted(playas, key=lambda x: x["NOMBRE_PLAYA"])
        )

    # Determinar si es código directo (ID_PLAYA)
    if nombre_o_codigo.isdigit():
        codigo = nombre_o_codigo
        nombre_mostrado = codigo
    else:
        nombre_normalizado = nombre_o_codigo.lower()
        if nombre_normalizado in NOMBRE_A_CODIGO:
            codigo = str(NOMBRE_A_CODIGO[nombre_normalizado])
            nombre_mostrado = nombre_o_codigo
        else:
            coincidencias = buscar_playas_por_nombre(nombre_normalizado)
            if len(coincidencias) == 0:
                return f"No se encontraron coincidencias para '{nombre_o_codigo}'. Usa 'listar' para ver todas las opciones."
            elif len(coincidencias) == 1:
                codigo = str(coincidencias[0]["ID_PLAYA"])
                nombre_mostrado = coincidencias[0]["NOMBRE_PLAYA"]
            else:
                opciones = "\n".join(
                    f"{p['NOMBRE_PLAYA']} ({p['NOMBRE_PROVINCIA']}, {p['NOMBRE_MUNICIPIO']})"
                    for p in coincidencias
                )
                return f"Se encontraron varias coincidencias para '{nombre_o_codigo}':\n{opciones}\nPor favor, especifica el nombre completo."

    # Construcción de URL
    if tipo_consulta == "playa":
        url = f"{AEMET_API_BASE}/prediccion/especifica/playa/{codigo}"
    elif tipo_consulta == "indice_uv":
        url = f"{AEMET_API_BASE}/prediccion/especifica/uvi/{dias_frc}"
    else:
        return "Tipo de consulta inválido. Usa 'playa' o 'indice_uv'."

    datos = await make_aemet_request(url)

    if not datos:
        return f"No se pudieron obtener datos de {tipo_consulta} para el código {codigo}."

    try:
        return f"Datos de {tipo_consulta} para '{nombre_mostrado}':\n{json.dumps(datos, indent=2, ensure_ascii=False)}"
    except Exception as e:
        return f"Error al procesar datos de {tipo_consulta}: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport='stdio')