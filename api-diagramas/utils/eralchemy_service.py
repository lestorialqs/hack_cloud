from eralchemy import render_er
from sqlalchemy import create_engine
import tempfile
import os

def generar_diagrama_er(data):
    sql_code = data.get("schema")
    if not sql_code:
        raise ValueError("No se proporcionó el esquema SQL.")

    # Crear archivo SQLite temporal en disco
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as db_file:
        db_path = db_file.name

    engine = create_engine(f"sqlite:///{db_path}")
    with engine.connect() as connection:
        connection.exec_driver_sql(sql_code)

    # Crear archivo de salida DOT temporal
    with tempfile.NamedTemporaryFile(suffix=".dot", delete=False) as dot_file:
        dot_path = dot_file.name

    # Usar ERAlchemy con archivos
    render_er(db_path, dot_path)

    # Leer el contenido .dot generado
    with open(dot_path, "r") as f:
        dot_code = f.read()

    # Limpieza opcional
    os.remove(db_path)
    os.remove(dot_path)

    return dot_code