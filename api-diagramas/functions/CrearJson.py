import json
from utils.json_to_mermaid import convert_json_to_mermaid
from utils.seguridad import validar_token  # <-- aquí

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

    resultado = validar_token(token)

    if not resultado.get('valido'):
        return {
            'statusCode': 403,
            'body': json.dumps({
                'error': 'Acceso no autorizado',
                'razon': resultado.get('razon'),
                'detalle': resultado.get('detalle', '')
            })
        }

    # === Continuar con la lógica principal ===
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