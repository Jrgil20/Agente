import os
from azure.identity import AzureCliCredential, DefaultAzureCredential, ChainedTokenCredential
import logging

logger = logging.getLogger(__name__)

def get_azure_credential():
    """
    Get Azure credentials using a chained approach:
    1. Try Azure CLI credentials
    2. Fall back to Default Azure credentials
    """
    try:
        # Try Azure CLI credential first
        cli_credential = AzureCliCredential()
        
        # Chain with DefaultAzureCredential as fallback
        credential = ChainedTokenCredential(
            cli_credential,
            DefaultAzureCredential()
        )
        
        logger.info("Azure authentication configured successfully")
        return credential
        
    except Exception as e:
        logger.error(f"Error setting up Azure authentication: {str(e)}")
        raise
