import os
from dotenv import load_dotenv

load_dotenv()

AZURE_PROJECT_CONNECTION_STRING = os.getenv("AZURE_PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT = os.getenv("MODEL_DEPLOYMENT") 