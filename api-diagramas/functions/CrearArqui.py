from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
import json
import os
from graphviz import ExecutableNotFound

def lambda_handler(event, context):
    # Configuración CRUCIAL
    os.environ['PATH'] = f"/opt/python/bin:{os.environ['PATH']}"
    os.environ['LD_LIBRARY_PATH'] = "/opt/python/lib"
    
    # Configura el backend de graphviz manualmente
    os.environ['GRAPHVIZ_DOT'] = "/opt/python/bin/dot"
    
    try:
        diagram_name = "ArquitecturaWeb"
        output_dot = f"/tmp/{diagram_name}.dot"
        
        with Diagram(diagram_name, show=False, filename=output_dot[:-4], direction="LR"):
            lb = ELB("Load Balancer")
            web = EC2("Web Server")
            db = RDS("Database")
            lb >> web >> db
            
        with open(output_dot, "r") as f:
            dot_content = f.read()
            
        return {
            "statusCode": 200,
            "body": json.dumps({"dot": dot_content})
        }
        
    except ExecutableNotFound as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Graphviz no encontrado",
                "details": str(e),
                "path": os.environ.get('PATH'),
                "files_in_bin": os.listdir('/opt/python/bin')[:10]
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }