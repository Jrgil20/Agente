# Agente de Análisis de Sentimiento para la Vinotinto

Este proyecto implementa un agente de análisis de sentimiento sobre comentarios de partidos de la Vinotinto, usando modelos generativos de Azure AI Foundry y OpenAI.

## Estructura del proyecto

- `src/`: Código fuente principal
- `tests/`: Pruebas unitarias
- `.env`: Variables de entorno (no subir a git)
- `requirements.txt`: Dependencias

## Instalación

1. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura tus credenciales de Azure y el nombre del deployment en el archivo `.env`.

## Uso

Ejecuta el agente desde la carpeta ``:
```bash
azd auth login
python src/setup_azure.py
python src/chat_app.py --input tweets.csv --output results.json
```

## Exportación

Los resultados pueden exportarse en formato JSON o CSV para su integración en dashboards.

---