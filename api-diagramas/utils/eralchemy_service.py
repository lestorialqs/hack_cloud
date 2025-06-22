from eralchemy import render_er

import os
import uuid
def generar_diagrama_er(data):
    """
    data debería incluir un string SQL en formato 'schema', por ejemplo:
    {"schema": "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);"}
    """
    sql_code = data.get("schema")
    if not sql_code:
        raise ValueError("No se proporcionó el esquema SQL.")

    # Guardamos el esquema en un archivo temporal
    tmp_id = str(uuid.uuid4())
    input_path = f"/tmp/{tmp_id}_schema.sql"
    output_path = f"/tmp/{tmp_id}_diagrama.er"

    with open(input_path, "w") as f:
        f.write(sql_code)

    # Ejecutamos ERAlchemy para convertirlo a .er (texto tipo Mermaid/ER)
    render_er(input_path, output_path, format='er')

    # Devolvemos el contenido generado
    with open(output_path, "r") as f:
        return f.read()