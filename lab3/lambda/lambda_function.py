import json
import qrcode
import boto3
import uuid
from io import BytesIO
import os

s3 = boto3.client('s3')

# Zmienne środowiskowe: BUCKET_NAME i REGION_NAME
BUCKET_NAME = os.environ.get('BUCKET_NAME')
REGION_NAME = os.environ.get('REGION_NAME')

def lambda_handler(event, context):
    # Pobierz URL z żądania
    try:
        body = json.loads(event['body'])
        url = body['url']
    except (KeyError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request: must include "url"'})
        }

    # Generuj QR
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Wygeneruj unikalną nazwę pliku
    filename = f"{uuid.uuid4()}.png"

    # Zapisz do S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=buffer,
        ContentType='image/png',
        ACL='public-read'  # plik będzie publiczny
    )

    # Zbuduj publiczny URL
    public_url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{filename}"

    return {
        'statusCode': 200,
        'body': json.dumps({'qr_code_url': public_url})
    }
