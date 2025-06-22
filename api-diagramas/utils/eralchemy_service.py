from eralchemy import render_er
from sqlalchemy import create_engine, MetaData
import json

def generar_diagrama_er(data):
    sql_code = data.get("schema")
    if not sql_code:
        raise ValueError("No se proporcionó el esquema SQL.")

    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as connection:
        connection.exec_driver_sql(sql_code)  # ← ✅ línea corregida

        metadata = MetaData()
        metadata.reflect(bind=engine)

        dot_code = render_er(metadata, output=None)
        return dot_code