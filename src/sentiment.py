from typing import Dict, Any
from config import AZURE_PROJECT_CONNECTION_STRING, MODEL_DEPLOYMENT
from auth_helper import get_azure_credential

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from openai import AzureOpenAI, BadRequestError
from azure.ai.ml import MLClient
import os
from dotenv import load_dotenv
import json
import logging

API_VERSION = "2024-12-01-preview"

# Prompt inicial personalizado
SYSTEM_PROMPT = """
Finalidad
Tu finalidad es realizar un análisis de sentimiento de comentarios sobre los partidos de la Vinotinto en español (con acento venezolano), asignando a cada comentario un puntaje entre –1 (muy negativo) y +1 (muy positivo), clasificándolos como "positivo", "neutral" o "negativo", y además extraer todos los hashtags y palabras clave relevantes.

Objetivos
* Ingestar datos desde CSV, texto plano o JSON, estableciendo un pipeline de ingesta confiable y escalable que garantice la integridad y calidad de los datos.
* Extraer y almacenar hashtags y palabras clave relevantes (por ejemplo, #Vinotinto, #Mundial2026) para identificar temas recurrentes y tendencias emergentes en las conversaciones sobre la Vinotinto.
* Calcular un puntaje de sentimiento entre –1 (muy negativo) y +1 (muy positivo) mediante técnicas de NLP para determinar el tono emocional de cada comentario, y clasificarlo como "positivo", "neutral" o "negativo".
* Detectar posibles expresiones de sarcasmo para mejorar la precisión del análisis de sentimientos y corregir interpretaciones erróneas.
* Considerar métricas de interacción (retweets y "me gusta") para ponderar el impacto de cada comentario en la valoración global del sentimiento.
* Ignorar enlaces e imágenes presentes en los textos para enfocar el análisis exclusivamente en el contenido textual relevante.
* Identificar y analizar patrones de sentimiento a lo largo del tiempo, detectando cambios en la percepción de la Vinotinto y posibles picos de opinión pública.
* Extraer y analizar patrones lexicográficos y de hashtag para descubrir correlaciones entre términos y niveles de sentimiento.
* Permitir la exportación de los resultados en formato JSON estructurado para facilitar su integración con otros sistemas y dashboards de seguimiento.

Indicaciones generales
* Asume que todos los comentarios se refieren a partidos de la Vinotinto y se expresan en español con acento venezolano.
* intuye el estado del partido: comentarios posteriores a un gol de la Vinotinto o cuando vamos ganando tienden a ser positivos, y comentarios cuando la selección va perdiendo o recibe gol tienden a ser negativos
* Detecta expresiones de sarcasmo y críticas en faltas o jugadas polémicas para ajustar correctamente la polaridad del sentimiento.
* Considera la cantidad de retweets y "me gusta" para ponderar la influencia de cada comentario en la valoración global del sentimiento, asignando mayor peso a los retweets según métricas de impacto en Twitter.
* Asume que los datos pueden llegar en CSV, texto plano o JSON, e integra un paso de extracción de datos (tweet_id, username, text, created_at, retweets, likes) previo al análisis de sentimiento.
* Extrae y analiza patrones de comportamiento y tendencias a partir de hashtags y palabras clave relevantes (por ejemplo, #Vinotinto, #Mundial2026).

Instrucciones paso a paso
*Acepta el archivo o texto en formato CSV, JSON o texto plano, asegurando que cada registro contenga al menos los campos `tweet_id`, `username`, `text`, `created_at` y, opcionalmente, `retweets` y `likes`.
*Elimina o ignora enlaces (`http://…`, `https://…`) e imágenes, y normaliza el texto (minúsculas, eliminación de caracteres especiales y tokenización).
*Extrae del campo `text` los hashtags (p. ej. `#Vinotinto`) y palabras clave relevantes ("golazo", "falta", "penal"), almacenándolos en listas separadas.
*Recupera las métricas de interacción (`retweets`, `likes`) y asócialas a cada comentario para posterior ponderación.
*Interpreta el campo `created_at` para intuir el momento del partido (antes o después de un gol) y el estado actual (ganando/perdiendo) de la Vinotinto.
* Calcula un puntaje continuo de sentimiento entre –1 y +1 con un modelo entrenado en español venezolano, aplicando ajustes positivos tras goles de la Vinotinto y negativos tras goles en contra.
*Detecta expresiones de sarcasmo y críticas en faltas o jugadas polémicas para corregir la polaridad del sentimiento cuando el modelo inicial pueda fallar.
*Pondera el puntaje según métricas de interacción: mayor peso a comentarios con más retweets y "me gusta".
*Clasifica cada comentario en "positivo" (score >0.2), "neutral" (–0.2 ≤ score ≤ 0.2) o "negativo" (score < –0.2).
*Agrega los resultados por partido o por día para identificar picos de sentimiento y tendencias, relacionándolos con hashtags y palabras clave.
*Construye la salida en JSON con los campos:

 `{ "tweet_id": "...", "username": "...", "text": "...", "created_at": "...", "score": 0.XX, "label": "positivo|neutral|negativo", "hashtags": ["#..."], "keywords": ["..."], "retweets": N, "likes": M }`
*Ofrece la opción de exportar todos los resultados en un archivo JSON o CSV para su integración en dashboards.
*Revisa muestras aleatorias de comentarios ya clasificados para validar y ajustar umbrales de sentimiento y reglas de detección de sarcasmo.

IMPORTANTE: Devuelve SIEMPRE la respuesta SOLO en formato JSON válido, sin explicaciones ni texto adicional, con la siguiente estructura exacta:
{
  "score": float,
  "label": "positivo|neutral|negativo",
  "hashtags": ["#..."],
  "keywords": ["..."],
  "retweets": int,
  "likes": int
}
"""


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_chat_client() -> Any:
    """
    Inicializa el cliente de chat de Azure OpenAI usando variables de entorno y el SDK recomendado.
    """
    load_dotenv()
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_KEY")
    if not azure_endpoint or not azure_api_key:
        raise ValueError("Faltan variables de entorno: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY")
    client = AzureOpenAI(
        api_version=API_VERSION,
        azure_endpoint=azure_endpoint,
        api_key=azure_api_key
    )
    return client


def get_agent_client() -> Any:
    """
    Inicializa el cliente del agente Sentimental usando Azure ML SDK.
    """
    load_dotenv()
    logger.info("Inicializando cliente de Azure ML...")
    
    try:
        credential = get_azure_credential()
        client = MLClient(
            credential=credential,
            subscription_id=os.getenv("AZURE_ML_SUBSCRIPTION"),
            resource_group_name=os.getenv("AZURE_ML_RESOURCE_GROUP"),
            workspace_name=os.getenv("AZURE_ML_WORKSPACE")
        )
        
        # Get or create the agent endpoint
        try:
            logger.info("Intentando obtener endpoint existente...")
            agent = client.online_endpoints.get("vinotinto-sentiment-agent")
            logger.info("Endpoint encontrado")
        except Exception:
            logger.info("Creando nuevo endpoint...")
            # Create new agent endpoint if it doesn't exist
            from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment
            
            endpoint = ManagedOnlineEndpoint(
                name="vinotinto-sentiment-agent",
                description="Vinotinto Sentiment Analysis Agent"
            )
            agent = client.online_endpoints.begin_create_or_update(endpoint).result()
            logger.info("Endpoint creado exitosamente")
            
            # Deploy the model
            deployment = ManagedOnlineDeployment(
                name="sentiment-deployment",
                endpoint_name=endpoint.name,
                model="gpt-4",
                instance_type="Standard_DS3_v2",
                instance_count=1
            )
            client.online_deployments.begin_create_or_update(deployment).result()
        
        return agent
            
    except Exception as e:
        logger.error(f"Error initializing Azure ML client: {str(e)}")
        raise


def get_sentiment_score(text: str, client, model_deployment: str = None) -> Dict[str, Any]:
    """
    Envía el texto al modelo generativo o al agente Sentimental y obtiene el puntaje de sentimiento
    """
    if model_deployment:  # Usar modelo OpenAI directo si se proporciona el deployment
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
        try:
            response = client.chat.completions.create(
                messages=messages,
                max_tokens=4096,
                temperature=0.1,
                top_p=1.0,
                model=model_deployment
            )
            result_str = response.choices[0].message.content
            # Intentar extraer JSON aunque venga rodeado de texto
            import re
            match = re.search(r'{.*}', result_str, re.DOTALL)
            if match:
                try:
                    result = json.loads(match.group(0))
                except Exception:
                    result = {"score": 0, "label": "neutral", "hashtags": [], "keywords": []}
            else:
                result = {"score": 0, "label": "neutral", "hashtags": [], "keywords": []}
        except BadRequestError as e:
            logger.warning(f"Error de filtro de contenido de Azure para el texto: '{text[:100]}...'. Detalles: {e}")
            result = {"score": 0, "label": "filtered_by_policy", "hashtags": [], "keywords": []}
        except Exception as e:
            logger.error(f"Error inesperado al procesar el texto: '{text[:100]}...'. Detalles: {e}")
            result = {"score": 0, "label": "error", "hashtags": [], "keywords": []}
    else:  # Usar agente ML
        try:
            # Format the input for the endpoint
            input_data = {
                "input_data": {
                    "text": text,
                    "parameters": {
                        "temperature": 0.1,
                        "max_tokens": 4096
                    }
                }
            }
            result = client.invoke(input_data)
            # Parse the result
            if isinstance(result, str):
                result = json.loads(result)
            elif isinstance(result, dict):
                result = result.get("output", {"score": 0, "label": "neutral"})
        except Exception as e:
            logger.error(f"Error invoking agent: {str(e)}")
            result = {"score": 0, "label": "neutral", "hashtags": [], "keywords": []}
    return result