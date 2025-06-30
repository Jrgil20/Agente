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

3. Configura tus credenciales:
   ```bash
   cp env.example .env
   # Edita el archivo .env con tus credenciales de Azure
   ```

## Configuración

### Variables de entorno requeridas:

**Para modo OpenAI directo:**
- `AZURE_OPENAI_ENDPOINT`: Endpoint de tu recurso Azure OpenAI
- `AZURE_OPENAI_KEY`: Clave API de Azure OpenAI
- `MODEL_DEPLOYMENT`: Nombre del deployment del modelo (ej: gpt-4)

**Para modo agente (opcional):**
- `AZURE_ML_SUBSCRIPTION`: ID de tu suscripción Azure
- `AZURE_ML_RESOURCE_GROUP`: Nombre del grupo de recursos
- `AZURE_ML_WORKSPACE`: Nombre del workspace de ML
- `AZURE_ML_LOCATION`: Región de Azure (ej: eastus)

## Uso

### Modo básico (OpenAI directo):
```bash
python src/chat_app.py --input tweets.csv --output results.json
```

### Modo agente (requiere configuración adicional):
```bash
azd auth login
python src/setup_azure.py
python src/chat_app.py --input tweets.csv --output results.json
```

### Forzar uso de OpenAI:
```bash
python src/chat_app.py --input tweets.csv --output results.json --force-openai
```

## Exportación

Los resultados pueden exportarse en formato JSON o CSV para su integración en dashboards.

## Solución de problemas

Si encuentras errores de instalación:
1. Asegúrate de estar usando Python 3.8 o superior
2. Actualiza pip: `pip install --upgrade pip`
3. Instala las dependencias una por una si es necesario

---