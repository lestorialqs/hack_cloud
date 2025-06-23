from utils.eralchemy_service import generar_diagrama_er
import json
import boto3

def lambda_handler(event, context):
    # === Validación del token ===
    try:
        token = event['headers']['token']
    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Token faltante en headers"})
        }

    # Invocar Lambda validador
    lambda_client = boto3.client('lambda')
    payload_string = json.dumps({"token": token})

    invoke_response = lambda_client.invoke(
        FunctionName="api-hack-usuarios-dev-validarToken",
        InvocationType='RequestResponse',
        Payload=payload_string
    )

    response_payload = json.loads(invoke_response['Payload'].read())
    print("Respuesta del validador:", response_payload)

    # Validar resultado
    status_code = response_payload.get('statusCode')
    body = json.loads(response_payload.get('body', '{}'))
    token_valido = body.get('tokenValido', False)

    if status_code == 403 or not token_valido:
        return {
            "statusCode": 403,
            "body": json.dumps({"error": "Acceso no autorizado"})
        }

    # === Procesar entrada y generar diagrama ER ===
    try:
        raw_body = event.get("body", {})
        body_data = json.loads(raw_body) if isinstance(raw_body, str) else raw_body

        if not isinstance(body_data, dict):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Formato de cuerpo inválido"})
            }

        resultado = generar_diagrama_er(body_data)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain"},
            "body": resultado
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }