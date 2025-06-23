import boto3
import json
from utils.json_to_mermaid import convert_json_to_mermaid

def lambda_handler(event, context):
    print(event)
    # Entrada (json)
    producto = event['body']
    
    # Inicio - Proteger el Lambda
    token = event['headers']['token']
    lambda_client = boto3.client('lambda')    
    payload_string = '{ "token": "' + token +  '" }'
    invoke_response = lambda_client.invoke(FunctionName="api-hack-usuarios-dev-validarToken",
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
    
    
