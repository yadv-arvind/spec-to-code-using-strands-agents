from bedrock_agentcore.runtime import BedrockAgentCoreApp

from agents import get_agent

app = BedrockAgentCoreApp()
log = app.logger


@app.entrypoint
async def invoke(payload, context):
    log.info("Invoking spec-to-code agent...")
    agent = get_agent()
    async for event in agent.stream_async(payload.get("prompt", ""), limits={"turns": 4}):
        if "data" in event and isinstance(event["data"], str):
            yield event["data"]


if __name__ == "__main__":
    app.run()
