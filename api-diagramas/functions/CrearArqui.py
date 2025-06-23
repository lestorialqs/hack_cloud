from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
import json

def lambda_handler(event, context):
    # Configuración
    diagram_name = "ArquitecturaWeb"
    output_dot = f"/tmp/{diagram_name}.dot"
    
    # Generar diagrama en formato DOT (sin crear imagen)
    with Diagram(diagram_name, show=False, filename=output_dot[:-4], direction="LR"):
        lb = ELB("Load Balancer")
        web = EC2("Web Server")
        db = RDS("Database")
        
        lb >> web >> db  # Conectamos los componentes
    
    # Leer el archivo DOT generado
    with open(output_dot, "r") as f:
        dot_content = f.read()
    
    # Respuesta al frontend
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "dot": dot_content,
            "message": "Diagrama en formato DOT listo para renderizar"
        })
    }