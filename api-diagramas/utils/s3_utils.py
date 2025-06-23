import boto3
import os

BUCKET = os.environ.get("BUCKET_NAME", "bucket-diagramas-aws")

def subir_a_s3(contenido_bytes, key, extension):
    s3 = boto3.client('s3')

    content_type = {
        'png': 'image/png',
        'svg': 'image/svg+xml'
    }.get(extension, 'application/octet-stream')

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=contenido_bytes,
        ContentType=content_type
    )