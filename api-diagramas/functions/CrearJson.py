
import json
from utils.json_to_mermaid import convert_json_to_mermaid

def lambda_handler(event, context):

    
    try:
        body = event.get('body')
        data = json.loads(body) if isinstance(body, str) else body
        mermaid_code = convert_json_to_mermaid(data)
        
        return {
            "statusCode": 200,
            "body": mermaid_code
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
    