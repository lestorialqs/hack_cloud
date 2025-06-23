import json
import base64
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # === Validar token ===
    try:
        token = event['headers']['token']
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Token faltante en headers'})
        }

    lambda_client = boto3.client('lambda')
    payload = json.dumps({'token': token})

    try:
        invoke_response = lambda_client.invoke(
            FunctionName="api-hack-usuarios-dev-validarToken",  # ← tu nombre real
            InvocationType='RequestResponse',
            Payload=payload
        )
        response_data = json.loads(invoke_response['Payload'].read())
        status_code = response_data.get('statusCode', 500)
        body_data = json.loads(response_data.get('body', '{}'))

        if status_code != 200 or not body_data.get('tokenValido', False):
            return {
                'statusCode': 403,
                'body': json.dumps({
                    'error': 'Acceso no autorizado',
                    'razon': body_data.get('motivo', 'Desconocido')
                })
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Fallo al validar token', 'detalle': str(e)})
        }







    # Configuración básica
    BUCKET_NAME = 'bucket-diagramas-aws'
    
    try:
        # Caso 1: Imagen binaria directa (vía Postman)
        if event.get('isBase64Encoded', False):
            imagen_bytes = base64.b64decode(event['body'])
            nombre_archivo = f"directo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        # Caso 2: JSON con base64 (desde frontend)
        else:
            # Si el body ya es un dict (cuando API Gateway lo parsea)
            if isinstance(event['body'], dict):
                body = event['body']
            else:
                body = json.loads(event['body'])
            
            imagen_b64 = body['imagen'].split(',')[-1]  # Remueve "data:image/png;base64,"
            imagen_bytes = base64.b64decode(imagen_b64)
            nombre_archivo = f"json_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        # Subir a S3
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=nombre_archivo,
            Body=imagen_bytes,
            ContentType='image/png',
            ACL='private'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'url': f"https://{BUCKET_NAME}.s3.amazonaws.com/{nombre_archivo}",
                'key': nombre_archivo
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }