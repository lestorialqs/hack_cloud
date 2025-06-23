from diagrams import Diagram
from diagrams.aws.compute import EC2
import tempfile

def lambda_handler(event, context):
    os.environ["DIAGRAM_CACHE"] = "/tmp"  # Lambda solo permite escribir en /tmp
    
    with Diagram("Ejemplo Lambda", show=False, filename="/tmp/diagrama"):
        EC2("Servidor")
    
    with open("/tmp/diagrama.png", "rb") as f:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "image/png"},
            "body": f.read().hex(),  # O envíalo como base64
            "isBase64Encoded": True
        }