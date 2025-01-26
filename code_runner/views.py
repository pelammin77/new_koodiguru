# code_runner/views.py

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .lambda_executor import LambdaCodeExecutor
from main_app.models import Task

class ExecuteCodeView(APIView):
    def __init__(self):
        super().__init__()
        self.code_executor = LambdaCodeExecutor()

    def post(self, request, *args, **kwargs):
        code = request.data.get("code", "")
        inputs = request.data.get("inputs", [])
        language = request.data.get("language", "").lower()
        test_code = request.data.get("test_code", "")
        task_id = request.data.get("task_id")

        # Validate input
        if not code:
            return Response({"error": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not language:
            return Response({"error": "Language is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Currently only supporting Python
        if language != "python":
            return Response({"error": "Unsupported language specified"}, status=status.HTTP_400_BAD_REQUEST)

        # Get task if task_id is provided
        task = None
        if task_id:
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                pass

        # Execute code using Lambda
        return self.code_executor.execute_code(
            code=code,
            inputs=inputs,
            test_code=test_code,
            user=request.user if request.user.is_authenticated else None,
            task=task
        )