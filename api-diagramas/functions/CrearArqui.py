import os

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": {
            "dot_version": os.popen("/opt/python/bin/dot -V").read(),
            "files_in_layer": os.listdir("/opt/python/bin/")[:10],
            "python_path": os.environ.get('PATH', ''),
            "current_directory": os.listdir('.')
        }
    }