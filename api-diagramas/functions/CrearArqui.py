import json
from utils.architect_service import generar_diagrama_arquitectura

def lambda_handler(event, context):
    try:
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)

        data = body if isinstance(body, dict) else {}
        resultado = generar_diagrama_arquitectura(data)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain"},
            "body": resultado
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }