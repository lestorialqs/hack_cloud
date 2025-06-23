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

    # Invocar Lambda validador
    lambda_client = boto3.client('lambda')
    payload_string = json.dumps({"token": token})

    invoke_response = lambda_client.invoke(
        FunctionName="api-hack-usuarios-dev-validarToken",  # cambia si tu función tiene otro nombre
        InvocationType='RequestResponse',
        Payload=payload_string
    )

    response_payload = json.loads(invoke_response['Payload'].read())
    print("Respuesta del validador:", response_payload)

    # Interpretar respuesta del validador
    status_code = response_payload.get('statusCode')
    body = json.loads(response_payload.get('body', '{}'))
    token_valido = body.get('tokenValido', False)

    if status_code == 403 or not token_valido:
        return {
            'statusCode': 403,
            'body': json.dumps({'error': 'Acceso no autorizado'})
        }
 
    
    try:
        body = event.get('body')
        data = json.loads(body) if isinstance(body, str) else body
        mermaid_code = convert_json_to_mermaid(data)
        
        return {
            "statusCode": 200,
            "body": mermaid_code
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
    
