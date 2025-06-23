import boto3
import json
from datetime import datetime
def lambda_handler(event, context):
    try:
        # Obtener token de headers o del cuerpo
        token = event.get('headers', {}).get('token') or event.get('token')
        
        if not token:
            return {
                "statusCode": 400,
                "body": json.dumps({"tokenValido": False, "motivo": "Token no proporcionado"})
            }

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('ValidarTable')
        response = table.get_item(Key={'token': token})
        item = response.get('Item')

        if not item:
            return {
                "statusCode": 403,
                "body": json.dumps({"tokenValido": False, "motivo": "Token no encontrado"})
            }

        expires_str = item.get('expira')  # ← Corregido a 'expira'
        expires = datetime.strptime(expires_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.utcnow()

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
        print(f"Error validando token: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"tokenValido": False, "motivo": "Error interno", "detalle": str(e)})
        }