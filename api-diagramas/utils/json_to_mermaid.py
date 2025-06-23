import json

def convert_json_to_mermaid(data, style='class'):
    """
    Convierte un objeto JSON a código Mermaid
    
    Args:
        data: Puede ser un string JSON o un diccionario ya parseado
        style: Tipo de diagrama ('class', 'er', o 'graph')
    
    Returns:
        str: Código Mermaid
    
    Raises:
        ValueError: Si el JSON es inválido o la estructura no es la esperada
    """
    # Parsear si es necesario
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido: {str(e)}")
    
    # Validar estructura
    if not isinstance(data, dict):
        raise ValueError("Se esperaba un objeto JSON (dict) en la raíz")
    
    # Generar diagrama según el estilo
    if style == 'er':
        lines = ["erDiagram"]
        for entity, props in data.items():
            if not isinstance(props, dict):
                raise ValueError(f"Las propiedades de {entity} deben ser un objeto")
            lines.append(f"    {entity} {{")
            for field, field_type in props.items():
                lines.append(f"    {field_type} {field}")
            lines.append("    }")
    
    elif style == 'graph':
        lines = ["graph TD"]
        for entity, props in data.items():
            lines.append(f'  {entity}["{entity}"]')
            for field, field_type in props.items():
                lines.append(f'  {field}[{field}: {field_type}]')
                lines.append(f'  {entity} --> {field}')
    
    else:  # 'class' (default)
        lines = ["classDiagram"]
        for entity, props in data.items():
            lines.append(f"  class {entity} {{")
            for field, field_type in props.items():
                lines.append(f"    {field_type} {field}")
            lines.append("  }")
    
    return "\n".join(lines)