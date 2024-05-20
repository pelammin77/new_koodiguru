# code_runner/views.py

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .execution_utils import execute_python_code, execute_c_code,execute_cpp_code
from func_timeout import func_timeout, FunctionTimedOut
import io
import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class ExecuteCodeView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get("code", "")
        inputs = request.data.get("inputs", [])
        language = request.data.get("language", "").lower()  # Lisätty kielen käsittely
        test_code = request.data.get("test_code", "")

        # Tarkista puuttuvat tai virheelliset tiedot
        if not code:
            return Response({"error": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not language:
            return Response({"error": "Language is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Suorita koodi annetulla kielellä
        result = execute_code(code, inputs, language, test_code)  # Muokattu kutsua vastaamaan funktiota, joka ottaa kielen huomioon

        return Response(result)

