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
            'body': {'error': 'Token faltante en headers'},
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    lambda_client = boto3.client('lambda')
    payload = json.dumps({'token': token})

    try:
        invoke_response = lambda_client.invoke(
            FunctionName="api-hack-usuarios-dev-validarToken",
            InvocationType='RequestResponse',
            Payload=payload
        )
        response_data = json.loads(invoke_response['Payload'].read())
        status_code = response_data.get('statusCode', 500)
        body_data = json.loads(response_data.get('body', '{}'))

        if status_code != 200 or not body_data.get('tokenValido', False):
            return {
                'statusCode': 403,
                'body': {
                    'error': 'Acceso no autorizado',
                    'razon': body_data.get('motivo', 'Desconocido')
                },
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'error': 'Fallo al validar token',
                'detalle': str(e)
            },
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    # === Procesar entrada y generar diagrama ===
    try:
        raw_body = event.get('body', '{}')
        body_data = json.loads(raw_body) if isinstance(raw_body, str) else raw_body

        if not isinstance(body_data, dict) or not body_data:
            return {
                'statusCode': 400,
                'body': {'error': 'Formato de cuerpo inválido'},
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        mermaid_code = convert_json_to_mermaid(body_data, style='er')
        
        return {
            'statusCode': 200,
            'body': {
                'mermaidcode': mermaid_code
            },
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Para CORS
            }
        }

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': {'error': 'JSON malformado'},
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        print(f'Error al generar diagrama: {str(e)}')
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error al generar diagrama',
                'detalle': str(e)
            },
            'headers': {
                'Content-Type': 'application/json'
            }
        }