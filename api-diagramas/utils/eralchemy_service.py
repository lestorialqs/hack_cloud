from eralchemy import render_er
from sqlalchemy import create_engine, MetaData
import tempfile
import json

def generar_diagrama_er(data):
    """
    Genera código ER en formato Mermaid usando SQLAlchemy y ERAlchemy.
    """
    sql_code = data.get("schema")
    if not sql_code:
        raise ValueError("No se proporcionó el esquema SQL.")

    # Crear base de datos temporal en memoria
    engine = create_engine("sqlite:///:memory:")
    connection = engine.connect()
    connection.execute(sql_code)

    # Extraer metadatos
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    # Generar diagrama ER en formato DOT (Graphviz)
    dot_code = render_er(metadata, output=None)  # None para obtener el código DOT
    
    connection.close()
    return dot_code
