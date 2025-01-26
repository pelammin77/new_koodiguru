import boto3
import json
import logging
import traceback
from django.conf import settings
from django.http import JsonResponse
from main_app.models import LambdaUsage

logger = logging.getLogger(__name__)

class LambdaCodeExecutor:
    def __init__(self):
        self.lambda_client = boto3.client(
            'lambda',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.function_name = settings.AWS_LAMBDA_FUNCTION_NAME

    def execute_code(self, code, inputs=None, test_code=None, debug=False, user=None, task=None):
        """
        Execute code using AWS Lambda
        
        Args:
            code (str): The code to execute
            inputs (list): List of inputs for the code
            test_code (str): Test code to run after main code
            debug (bool): Whether to enable debug mode
            user: The user executing the code
            task: The task being attempted
        """
        try:
            print(user, task)
            # Save usage record first if we have both user and task
            if user and task:
                try:
                    LambdaUsage.objects.create(
                        user=user,
                        task=task
                    )
                except Exception as e:
                    logger.error(f"Failed to save Lambda usage record: {e}")

            payload = {
                'code': code,
                'inputs': inputs or [],
                'test_code': test_code,
                'debug': debug,
                'user_id': user.id if user else None,
                'task_id': task.id if task else None
            }

            if debug:
                logger.debug(f"Sending payload to Lambda: {payload}")

            response = self.lambda_client.invoke(
                FunctionName=self.function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps({'body': json.dumps(payload)})
            )

            response_payload = json.loads(response['Payload'].read())
            
            if debug:
                logger.debug(f"Received response from Lambda: {response_payload}")

            if 'statusCode' in response_payload:
                body = json.loads(response_payload['body'])
                return JsonResponse(body)
            else:
                return JsonResponse({
                    'error': 'Invalid response from Lambda',
                    'output': ''
                })

        except Exception as e:
            logger.exception("Error in Lambda execution")
            return JsonResponse({
                'error': str(e),
                'output': '',
                'debug_info': traceback.format_exc() if debug else None
            })