from sentiment import get_agent_client, get_chat_client
from setup_azure import setup_azure_environment
import logging
import subprocess
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_azure_cli():
    """Verifica la instalación de Azure CLI y azd"""
    try:
        # Check if Azure CLI is installed
        if not shutil.which('az'):
            logger.error("Azure CLI no está instalado")
            return False
            
        # Check if azd is installed
        if not shutil.which('azd'):
            logger.error("Azure Developer CLI (azd) no está instalado")
            return False
            
        # Test Azure CLI version
        subprocess.run(['az', '--version'], check=True)
        logger.info("✓ Azure CLI está instalado y funcionando")
        
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error verificando Azure CLI: {str(e)}")
        return False

def test_connections():
    """Prueba las conexiones a Azure ML y Azure OpenAI"""
    try:
        # Verificar configuración de ambiente
        logger.info("Configurando ambiente Azure...")
        if not setup_azure_environment():
            return False
            
        logger.info("Probando conexión con Azure ML...")
        agent = get_agent_client()
        logger.info("✓ Conexión con Azure ML exitosa")
        
        logger.info("Probando conexión con Azure OpenAI...")
        chat = get_chat_client()
        logger.info("✓ Conexión con Azure OpenAI exitosa")
        
        return True
        
    except Exception as e:
        logger.error(f"Error en la conexión: {str(e)}")
        return False

if __name__ == "__main__":
    test_connections()
