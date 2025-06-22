def convert_json_to_mermaid(data):
    lines = ["graph TD"]
    for entity, props in data.items():
        if isinstance(props, dict):
            for prop in props:
                lines.append(f"  {entity} --> {prop}")
        elif isinstance(props, list):
            for item in props:
                lines.append(f"  {entity} --> {item}")
        else:
            lines.append(f"  {entity} --> {props}")
    return "\n".join(lines)