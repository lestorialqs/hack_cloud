
def convert_json_to_mermaid(data, style='table'):
    if style == 'table':
        lines = ["classDiagram"]
        for entity, props in data.items():
            lines.append(f"  class {entity} {{")
            lines.extend([f"    {v} {k}" for k, v in props.items()])
            lines.append("  }")
    else:  # 'graph' (default)
        lines = ["graph TD"]
        for entity, props in data.items():
            lines.append(f'  {entity}["{entity}"]')
            lines.extend([f'  {k}[{k}: {v}]\n  {entity} --> {k}' for k, v in props.items()])
    return "\n".join(lines)