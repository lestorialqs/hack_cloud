import os
import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ValidarTable')

def lambda_handler(event, context):
    print(event)
    token = event['headers']['Authorization']
    if not token:
        return {
            "statusCode": 403,
            "message": "Token no proporcionado"
        }
    
    lambda_client = boto3.client('lambda')
    payload_string = '{ "token": "' + token +  '" }'
     invoke_response = lambda_client.invoke(FunctionName="ValidarToken",
                                           InvocationType='RequestResponse',
                                           Payload = payload_string)
    response = json.loads(invoke_response['Payload'].read())
    print(response)
    if response['statusCode'] == 403:
        return {
            'statusCode' : 403,
            'status' : 'Forbidden - Acceso No Autorizado'
        }
