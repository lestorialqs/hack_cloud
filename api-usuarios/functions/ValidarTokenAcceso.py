import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    try:
        token = event.get('token')
        if not token:
            return {
                "statusCode": 400,
                "body": json.dumps({"tokenValido": False, "motivo": "Token no proporcionado"})
            }

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('ValidarTable')  # ← Tu tabla real
        response = table.get_item(Key={'token': token})
        item = response.get('Item')

        if not item:
            return {
                "statusCode": 403,
                "body": json.dumps({"tokenValido": False, "motivo": "Token no encontrado"})
            }

        expires = item.get('expires')
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # UTC es mejor

        if now > expires:
            return {
                "statusCode": 403,
                "body": json.dumps({"tokenValido": False, "motivo": "Token expirado"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"tokenValido": True})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"tokenValido": False, "motivo": "Error interno", "detalle": str(e)})
        }