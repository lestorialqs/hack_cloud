from utils.eralchemy_service import generar_diagrama_er
import json

def lambda_handler(event, context):
    print(event)
    # Entrada (json)
    producto = event['body']
    
    # Inicio - Proteger el Lambda
    token = event['headers']['token']
    lambda_client = boto3.client('lambda')    
    payload_string = '{ "token": "' + token +  '" }'
    invoke_response = lambda_client.invoke(FunctionName="seguridad",
                                           InvocationType='RequestResponse',
                                           Payload = payload_string)
    response = json.loads(invoke_response['Payload'].read())
    print(response)
    if response['statusCode'] == 403:
        return {
            'statusCode' : 403,
            'status' : 'Forbidden - Acceso No Autorizado'
        }
    # Fin - Proteger el Lambda    
    try:
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body)

        data = body if isinstance(body, dict) else {}
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
