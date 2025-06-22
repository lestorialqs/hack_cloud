from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
import os

def generar_diagrama_arquitectura(data):
    """
    Genera un diagrama de arquitectura en formato texto DOT para que el frontend lo renderice.
    """
    dot_path = "/tmp/diagrama_arquitectura.dot"

    with Diagram("Infraestructura AWS", show=False, outformat="dot", filename="/tmp/diagrama_arquitectura"):
        lb = ELB("Load Balancer")

        with Cluster("Backend"):
            ec2_1 = EC2("App 1")
            ec2_2 = EC2("App 2")
        
        db = RDS("Database")
        lb >> [ec2_1, ec2_2] >> db

    with open(dot_path, "r") as f:
        return f.read()