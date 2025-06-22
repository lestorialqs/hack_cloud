import boto3
import hashlib
import json

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    try:
        # Parsear el body
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event

        # Campos obligatorios
        correo = body.get('correo')           # HASH key
        password = body.get('password')
        tipo_item = 'perfil'                  # RANGE key fija para el perfil

        # Campos opcionales
        nombre = body.get('nombre')
        apellido = body.get('apellido')


        if correo and password:
            hashed_password = hash_password(password)
            dynamodb = boto3.resource('dynamodb')
            tabla = dynamodb.Table('UsuariosTable')

            item = {
                'correo': correo,
                'tipo_item': tipo_item,
                'password': hashed_password
            }

            # Agrega los campos opcionales si vienen
            if nombre: item['nombre'] = nombre
            if apellido: item['apellido'] = apellido

            response = tabla.put_item(Item=item)

            return {
                'statusCode': 200,
                'body': json.dumps({"mensaje": "Usuario registrado correctamente", "response": response})
            }

        else:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Faltan correo o password"})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }