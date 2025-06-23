from utils.eralchemy_service import generar_diagrama_er
import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # === Validación del token ===
    try:
        # Obtener token de headers (API Gateway) o directamente del evento
        headers = event.get('headers', {})
        token = headers.get('token') or event.get('token')
        
        if not token:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Token faltante en headers"})
            }

        # Invocar Lambda validador con estructura correcta
        lambda_client = boto3.client('lambda')
        payload = {
            "token": token,
            "headers": {"token": token}  # Compatibilidad con ambas formas
        }

        invoke_response = lambda_client.invoke(
            FunctionName="api-hack-usuarios-dev-validarToken",
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        # Procesar respuesta del validador
        response_payload = json.loads(invoke_response['Payload'].read())
        print("Respuesta del validador:", response_payload)

        if invoke_response['StatusCode'] != 200:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Error al validar token"})
            }

        # Parsear la respuesta correctamente
        validation_body = json.loads(response_payload.get('body', '{}'))
        if not validation_body.get('tokenValido', False):
            motivo = validation_body.get('motivo', 'Token inválido')
            return {
                "statusCode": 403,
                "body": json.dumps({
                    "error": "Acceso no autorizado",
                    "razon": motivo
                })
            }

    except Exception as e:
        print(f"Error en validación de token: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Error interno al validar token",
                "detalle": str(e)
            })
        }

    # === Procesar entrada y generar diagrama ER ===
    try:
        # Obtener y parsear el cuerpo correctamente
        raw_body = event.get("body", "{}")
        body_data = json.loads(raw_body) if isinstance(raw_body, str) else raw_body

        if not isinstance(body_data, dict) or not body_data:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Formato de cuerpo inválido"})
            }

        # Generar el diagrama ER
        resultado = generar_diagrama_er(body_data)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/plain",
                "Access-Control-Allow-Origin": "*"  # Para CORS
            },
            "body": resultado
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "JSON malformado"})
        }
    except Exception as e:
        print(f"Error al generar diagrama: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Error al generar diagrama ER",
                "detalle": str(e)
            })
        }