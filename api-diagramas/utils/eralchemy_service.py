from eralchemy import render_er
from sqlalchemy import create_engine, MetaData
import tempfile
import os
import json

def generar_diagrama_er(data):
    """
    Genera diagrama ER en formato DOT usando ERAlchemy
    """
    sql_code = data.get("schema")
    if not sql_code:
        raise ValueError("No se proporcionó el esquema SQL.")

    # 1. Crear base de datos SQLite temporal
    db_path = "/tmp/temp_db.db"  # Lambda permite escribir en /tmp
    if os.path.exists(db_path):
        os.remove(db_path)
    
    engine = create_engine(f"sqlite:///{db_path}")
    
    # 2. Ejecutar el esquema SQL
    try:
        with engine.connect() as conn:
            # Ejecutar cada sentencia SQL por separado
            for statement in sql_code.split(";"):
                if statement.strip():
                    conn.exec_driver_sql(statement)
        
        # 3. Generar el diagrama DOT
        dot_path = "/tmp/diagram.dot"
        if os.path.exists(dot_path):
            os.remove(dot_path)
            
        render_er(f"sqlite:///{db_path}", dot_path)
        
        # 4. Leer el contenido DOT
        with open(dot_path, "r") as f:
            dot_content = f.read()
            
        return dot_content
        
    finally:
        # Limpieza
        if os.path.exists(db_path):
            os.remove(db_path)
        if os.path.exists(dot_path):
            os.remove(dot_path)