def convert_json_to_mermaid(data):
    lines = ["graph TD"]
    for entity, props in data.items():
        if isinstance(props, dict):
            # Crea un nodo para la entidad
            lines.append(f"  {entity}[{entity}]")
            for prop, prop_type in props.items():
                # Crea nodos para las propiedades con sus tipos
                lines.append(f"  {prop}[{prop}: {prop_type}]")
                lines.append(f"  {entity} --> {prop}")
        elif isinstance(props, list):
            for item in props:
                lines.append(f"  {entity} --> {item}")
        else:
            lines.append(f"  {entity} --> {props}")
    return "\n".join(lines)