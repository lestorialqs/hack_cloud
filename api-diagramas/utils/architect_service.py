import os
import subprocess
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.custom import Custom

# Agregar la ruta del binario `dot` desde el layer al PATH
os.environ["PATH"] = f"/opt/python/bin:{os.environ.get('PATH', '')}"

print("PATH:", os.environ["PATH"])
# Mapeo de componentes
CLASES_DIAGRAMAS = {
    "EC2": EC2,
    "RDS": RDS,
    "ELB": ELB,
}

def generar_diagrama_arquitectura(data):
    """
    Genera un diagrama .dot a partir de un JSON.
    """
    verify_dependencies()  # Verifica dependencias antes de continuar

    titulo = data.get("titulo", "Arquitectura")
    componentes = data.get("componentes", [])
    conexiones = data.get("conexiones", [])

    output_path = "/tmp/diagrama.dot"
    if os.path.exists(output_path):
        os.remove(output_path)

    with Diagram(titulo, show=False, outformat="dot", filename="/tmp/diagrama"):
        nodos = {
            comp["nombre"]: CLASES_DIAGRAMAS.get(comp["tipo"], Custom)(comp["nombre"])
            for comp in componentes
        }
        for origen, destino in conexiones:
            if origen in nodos and destino in nodos:
                nodos[origen] >> nodos[destino]

    with open(output_path, "r") as f:
        return f.read()