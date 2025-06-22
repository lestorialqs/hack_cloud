import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import os

SECRET_KEY = os.environ.get("JWT_SECRET", "clave-supersecreta")

def validar_token(token):
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        return {
            "user_id": decode.get("sub"),
            "tenant_id": decode.get("tenant_id"),
            "claims": decode
        }

    except ExpiredSignatureError:
        raise Exception("Token expirado")
    except InvalidTokenError as e:
        raise Exception(f"Token inválido: {str(e)}")

