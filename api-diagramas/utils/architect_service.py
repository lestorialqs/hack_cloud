import os
import subprocess
from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.custom import Custom

# Configuración crítica para Graphviz
os.environ['PATH'] += os.pathsep + '/opt/bin'
os.environ['LD_LIBRARY_PATH'] = '/opt/lib:' + os.environ.get('LD_LIBRARY_PATH', '')

# Verificación de Graphviz y diagrams
def verify_dependencies():
    """Verifica que Graphviz y diagrams estén correctamente instalados."""
    # 1. Verifica Graphviz
    dot_path = '/opt/bin/dot'
    if not os.path.exists(dot_path):
        raise Exception("❌ Graphviz no encontrado en /opt/bin/dot")
    
    try:
        version = subprocess.run(
            [dot_path, '-V'],
            capture_output=True,
            text=True
        )
        print(f"✅ Graphviz encontrado. Versión: {version.stderr.strip()}")
    except Exception as e:
        raise Exception(f"❌ Error al ejecutar 'dot': {str(e)}")

    # 2. Verifica diagrams (intenta crear un diagrama mínimo)
    try:
        with Diagram("Test", show=False, filename="/tmp/test_diagram"):
            EC2("Test EC2")
        print("✅ diagrams funciona correctamente")
    except Exception as e:
        raise Exception(f"❌ Error en diagrams: {str(e)}")

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