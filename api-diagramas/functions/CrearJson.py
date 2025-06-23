# functions/convertir_json/handler.py
import boto3
import json
from utils.json_to_mermaid import convert_json_to_mermaid

def lambda_handler(event, context):
    print("Evento recibido:", event)

    # === Validar token ===
    try:
        token = event['headers']['token']
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Token faltante en headers'})
        }

    lambda_client = boto3.client('lambda')
    payload = json.dumps({'token': token})

    try:
        invoke_response = lambda_client.invoke(
            FunctionName="api-hack-usuarios-dev-validarToken",  # ← tu nombre real
            InvocationType='RequestResponse',
            Payload=payload
        )
        response_data = json.loads(invoke_response['Payload'].read())
        status_code = response_data.get('statusCode', 500)
        body_data = json.loads(response_data.get('body', '{}'))

        if status_code != 200 or not body_data.get('tokenValido', False):
            return {
                'statusCode': 403,
                'body': json.dumps({
                    'error': 'Acceso no autorizado',
                    'razon': body_data.get('motivo', 'Desconocido')
                })
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Fallo al validar token', 'detalle': str(e)})
        }

    # === Convertir JSON a Mermaid ===
# === Convertir JSON a Mermaid ===
    try:
        body = event.get('body')
        data = json.loads(body) if isinstance(body, str) else body
        
        mermaid_code = convert_json_to_mermaid(data, style='er')
        
        return {
            "statusCode": 200,
            "body": {
                "mermaidcode": mermaid_code
            },
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except ValueError as e:
        return {
            "statusCode": 400,
            "body": {"error": str(e)},
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"error": "Error interno del servidor"},
            "headers": {
                "Content-Type": "application/json"
            }
        }