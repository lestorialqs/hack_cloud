import json
import base64
import uuid
from utils.s3_utils import subir_a_s3

def handler(event, context):
    try:
        body = json.loads(event['body'])

        nombre = body.get('nombre', f"img-{uuid.uuid4()}")
        extension = body.get('extension', 'png')
        imagen_base64 = body['imagen']

        if extension not in ['png', 'svg']:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Extensión no permitida"})
            }

        # Decodificar imagen
        imagen_bytes = base64.b64decode(imagen_base64)

        key = f"{nombre}.{extension}"
        subir_a_s3(imagen_bytes, key, extension)

        return {
            "statusCode": 200,
            "body": json.dumps({"mensaje": "Imagen guardada", "key": key})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }