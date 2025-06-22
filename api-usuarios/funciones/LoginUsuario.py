import boto3
import hashlib
import uuid
from datetime import datetime, timedelta
import json

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    try:
        print("Received event:", event)

        # Parsear el cuerpo
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event

        correo = body.get('correo')
        password = body.get('password')

        if not correo or not password:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Faltan correo o password'})
            }

        hashed_password = hash_password(password)

        dynamodb = boto3.resource('dynamodb')
        tabla_usuarios = dynamodb.Table('UsuariosTable')

        # Leer el perfil del usuario
        response = tabla_usuarios.get_item(
            Key={
                'correo': correo,
                'tipo_item': 'perfil'
            }
        )

        if 'Item' not in response:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Usuario no existe'})
            }

        user = response['Item']
        if hashed_password != user['password']:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Password incorrecto'})
            }

        # Si la contraseña coincide, generamos y almacenamos un token
        token = str(uuid.uuid4())
        expires = datetime.utcnow() + timedelta(minutes=60)

        tabla_tokens = dynamodb.Table('ValidarTable')
        tabla_tokens.put_item(
            Item={
                'token': token,
                'correo': correo,
                'expira': expires.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'token': token})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }