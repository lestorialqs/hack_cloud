from diagrams import Diagram
from diagrams.aws.compute import EC2
import os

def lambda_handler(event, context):
    # Configura variables de entorno críticas
    os.environ["PATH"] = f"/opt/bin:{os.environ['PATH']}"
    
    with Diagram("Demo", show=False, filename="/tmp/diagram"):
        EC2("Web Server")
    
    with open("/tmp/diagram.dot", "r") as f:
        return {
            "statusCode": 200,
            "body": f.read()  # Retorna el DOT para renderizar en frontend
        }