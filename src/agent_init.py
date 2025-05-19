import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from typing import Optional

def initialize_agent(instructions: str) -> Optional[str]:
    """Initialize an AI agent with the given instructions"""
    try:
        connection_string = os.getenv("PROJECT_CONNECTION_STRING")
        if not connection_string:
            return None
            
        with AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=connection_string
        ) as project_client:
            agent = project_client.agents.create_agent(
                model="gpt-4",
                name="Sentimental",
                instructions=instructions
            )
            return agent.id
    except Exception as e:
        print(f"Error initializing agent: {str(e)}")
        return None
