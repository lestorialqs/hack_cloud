import json
from utils.architect_service import generar_diagrama_arquitectura

def lambda_handler(event, context):
    try:
        # Parse input
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)

        # Genera el diagrama
        dot_output = generar_diagrama_arquitectura(body)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain"},
            "body": dot_output
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}",
            "stackTrace": str(e.__traceback__) if hasattr(e, '__traceback__') else None
        }