from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.custom import Custom
import tempfile
import os

# Mapeo de tipo a clase
CLASES_DIAGRAMAS = {
    "EC2": EC2,
    "RDS": RDS,
    "ELB": ELB,
    # Puedes agregar más tipos aquí o usar Custom para genéricos
}

def generar_diagrama_arquitectura(data):
    """
    Genera un diagrama .dot dinámico a partir de un JSON que describe componentes y conexiones.
    """
    titulo = data.get("titulo", "Arquitectura")
    componentes_raw = data.get("componentes", [])
    conexiones = data.get("conexiones", [])

    # Diccionario para acceder a los nodos por nombre
    nodos = {}

    # Ruta del archivo .dot temporal
    dot_path = "/tmp/diagrama_arquitectura.dot"
    if os.path.exists(dot_path):
        os.remove(dot_path)

    # Construcción del diagrama
    with Diagram(titulo, show=False, outformat="dot", filename="/tmp/diagrama_arquitectura"):
        for comp in componentes_raw:
            tipo = comp.get("tipo")
            nombre = comp.get("nombre")
            clase = CLASES_DIAGRAMAS.get(tipo, Custom)  # Usa Custom si no está mapeado
            nodo = clase(nombre)
            nodos[nombre] = nodo

        for origen, destino in conexiones:
            if origen in nodos and destino in nodos:
                nodos[origen] >> nodos[destino]

    # Leer archivo generado
    with open(dot_path, "r") as f:
        return f.read()
