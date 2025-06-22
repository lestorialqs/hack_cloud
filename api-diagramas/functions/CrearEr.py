from utils.eralchemy_service import generar_diagrama_er
import json

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if body is None:
            return {
                "statusCode": 400,
                "body": "Falta el campo 'body' en el evento"
            }

        data = json.loads(body) if isinstance(body, str) else body

        resultado = generar_diagrama_er(data)

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