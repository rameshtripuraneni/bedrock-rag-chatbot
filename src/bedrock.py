import json
import boto3
from src.settings import settings

_bedrock = boto3.client("bedrock-runtime", region_name=settings.aws_region)

def embed_text(text: str) -> list[float]:
    body = {"inputText": text}
    resp = _bedrock.invoke_model(
        modelId=settings.bedrock_embed_model_id,
        body=json.dumps(body).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    payload = json.loads(resp["body"].read())
    emb = payload.get("embedding")
    if not emb:
        raise RuntimeError(f"Unexpected embed response: {payload}")
    return emb

def chat_complete(system: str, user: str) -> str:
    # Claude 3 style example (adjust if you use different model)
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 600,
        "system": system,
        "messages": [{"role": "user", "content": user}],
        "temperature": 0.2,
    }
    resp = _bedrock.invoke_model(
        modelId=settings.bedrock_chat_model_id,
        body=json.dumps(body).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    payload = json.loads(resp["body"].read())

    content = payload.get("content", [])
    if content and isinstance(content, list):
        texts = [c.get("text", "") for c in content if isinstance(c, dict)]
        out = "".join(texts).strip()
        if out:
            return out

    if "completion" in payload:
        return str(payload["completion"]).strip()

    raise RuntimeError(f"Unexpected chat response: {payload}")
