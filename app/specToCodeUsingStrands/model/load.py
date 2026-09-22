from strands.models.bedrock import BedrockModel

# Nova-2-Lite emits tool-use blocks Bedrock rejects as malformed on the second
# call, which breaks the write -> test -> revise loop. Nova Pro chains reliably.
MODEL_ID = "us.amazon.nova-pro-v1:0"


def load_model() -> BedrockModel:
    """Get Bedrock model client using IAM credentials."""
    return BedrockModel(
        model_id=MODEL_ID,
        region_name="us-east-1",
        temperature=0,
    )
