import os
import logging
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
import subprocess
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_dependencies():
    """Verifica y instala dependencias necesarias"""
    try:
        import pkg_resources
        required = {'azure-mgmt-resource', 'azure-identity', 'azure-ai-ml'}
        installed = {pkg.key for pkg in pkg_resources.working_set}
        missing = required - installed
        
        if missing:
            logger.info("Instalando dependencias faltantes...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            return True
            
    except Exception as e:
        logger.error(f"Error verificando dependencias: {str(e)}")
        return False

def setup_azure_environment():
    """Configura el ambiente de Azure necesario para el agente"""
    if not verify_dependencies():
        raise RuntimeError("No se pudieron instalar las dependencias necesarias")
        
    try:
        # Verificar credenciales
        credential = AzureCliCredential()
        subscription_id = os.getenv("AZURE_ML_SUBSCRIPTION")
        
        # Crear cliente de recursos
        resource_client = ResourceManagementClient(credential, subscription_id)
        
        # Verificar grupo de recursos
        rg_name = os.getenv("AZURE_ML_RESOURCE_GROUP")
        location = os.getenv("AZURE_ML_LOCATION")
        
        if not any(rg.name == rg_name for rg in resource_client.resource_groups.list()):
            logger.info(f"Creando grupo de recursos {rg_name}...")
            resource_client.resource_groups.create_or_update(
                rg_name,
                {"location": location}
            )
        
        logger.info("✓ Ambiente Azure configurado correctamente")
        return True
        
    except Exception as e:
        logger.error(f"Error en configuración: {str(e)}")
        return False

if __name__ == "__main__":
    setup_azure_environment()
