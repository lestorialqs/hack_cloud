# utils/seguridad.py

import boto3
from datetime import datetime
import json

def validar_token(token: str):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ValidarTable')
    
    try:
        response = table.get_item(Key={'token': token})
        item = response.get('Item')

        if not item:
            return {"valido": False, "razon": "Token no encontrado"}

        expires = item.get('expires')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if now > expires:
            return {"valido": False, "razon": "Token expirado"}

        return {"valido": True}

    except Exception as e:
        return {"valido": False, "razon": "Error inesperado", "detalle": str(e)}