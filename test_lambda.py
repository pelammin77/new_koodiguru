import boto3
import json
import os
from dotenv import load_dotenv

# Lataa .env-tiedosto
load_dotenv()

# Hakee AWS-tiedot ympäristömuuttujista
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
LAMBDA_FUNCTION_NAME = os.getenv('AWS_LAMBDA_FUNCTION_NAME')

# Luo boto3 client
lambda_client = boto3.client(
    'lambda',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Lähetettävä data Lambdaan
payload = {
    "code": "print(2+2)",  # Yksinkertainen koodi
    "inputs": [],
    "user_id": "test_user",
    "task_id": "test_task"
}

# Lähetä pyyntö Lambdaan
response = lambda_client.invoke(
    FunctionName=LAMBDA_FUNCTION_NAME,
    InvocationType='RequestResponse',
    Payload=json.dumps({"body": json.dumps(payload)})
)

# Lue vastaus
response_payload = json.load(response['Payload'])

print("\n--- Lambda vastaus ---")
print(json.dumps(response_payload, indent=2))
