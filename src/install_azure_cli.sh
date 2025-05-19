#!/bin/bash

# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Azure Developer CLI (azd)
curl -fsSL https://aka.ms/install-azd.sh | sudo bash

# Verify installations
echo "Verifying installations..."
az --version
azd --version
