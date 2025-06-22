import json
from json2graph.mermaid import convert

def lambda_handler(event, context):
    try:
        body = event.get("body")
        data = json.loads(body) if isinstance(body, str) else body

        mermaid_code = convert(data)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain"},
            "body": mermaid_code
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }