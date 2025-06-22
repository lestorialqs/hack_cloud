from eralchemy import er_to_mermaid
from sqlalchemy import create_engine, MetaData
import json

def generar_diagrama_er(data):
    """
    Usa ERAlchemy para convertir SQL a código Mermaid.
    """
    sql_code = data.get("schema")
    if not sql_code:
        raise ValueError("No se proporcionó el esquema SQL.")

    # Crear base de datos temporal en memoria
    engine = create_engine("sqlite:///:memory:")
    connection = engine.connect()
    connection.execute(sql_code)

    # Extraer metadatos y convertir a Mermaid
    metadata = MetaData()
    metadata.reflect(bind=engine)
    mermaid_code = er_to_mermaid(metadata.tables.values())
    connection.close()

    return mermaid_code