#!/bin/bash
set -e

echo "Installing Strands Agents and tools..."
pip install strands-agents strands-agents-tools

echo ""
echo "Verifying AWS credentials are visible to boto3..."
python3 -c "import boto3; identity = boto3.client('sts').get_caller_identity(); print(f'Account: {identity[\"Account\"]}'); print(f'User/Role: {identity[\"Arn\"]}')"

echo ""
echo "✓ Setup complete. AWS credentials are ready."
