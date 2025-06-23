import os
import subprocess

def lambda_handler(event, context):
    # Configurar entorno - IMPORTANTE
    os.environ['LD_LIBRARY_PATH'] = '/opt/python/lib'
    
    try:
        result = subprocess.run(
            ['/opt/python/bin/dot', '-V'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return {
            "success": result.returncode == 0,
            "version_output": result.stderr.strip(),
            "loaded_libs": os.listdir('/opt/python/lib'),
            "env": dict(os.environ)
        }
    except Exception as e:
        return {
            "error": str(e),
            "traceback": str(e.__traceback__)
        }