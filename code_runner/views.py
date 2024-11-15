# code_runner/views.py

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .lambda_executor import LambdaCodeExecutor

class ExecuteCodeView(APIView):
    def __init__(self):
        super().__init__()
        self.code_executor = LambdaCodeExecutor()

    def post(self, request, *args, **kwargs):
        code = request.data.get("code", "")
        inputs = request.data.get("inputs", [])
        language = request.data.get("language", "").lower()
        test_code = request.data.get("test_code", "")

        # Validate input
        if not code:
            return Response({"error": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not language:
            return Response({"error": "Language is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Currently only supporting Python
        if language != "python":
            return Response({"error": "Unsupported language specified"}, status=status.HTTP_400_BAD_REQUEST)

        # Execute code using Lambda
        return self.code_executor.execute_code(code, inputs, test_code)