import boto3
from datetime import datetime

def lambda_handler(event, context):
    try:
        # Obtener token desde el evento
        token = event.get('token')
        if not token:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Token no proporcionado"})
            }

        # Acceder a DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('ValidarTable')
        response = table.get_item(Key={'token': token})

        # Verificar si existe
        item = response.get('Item')
        if not item:
            return {
                "statusCode": 403,
                "body": json.dumps({"tokenValido": False, "motivo": "Token no encontrado"})
            }

        # Verificar expiración
        expires = item.get('expires')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if now > expires:
            return {
                "statusCode": 403,
                "body": json.dumps({"tokenValido": False, "motivo": "Token expirado"})
            }

        # Todo correcto
        return {
            "statusCode": 200,
            "body": json.dumps({"tokenValido": True})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }