# koodin ajaja

from func_timeout import func_timeout, FunctionTimedOut
from django.http import JsonResponse
import io
import sys
from main_app.models import TaskTest


def process_code(code, inputs=[], task=None):
    print("Saadut syötteet:", inputs)
    def input_func(prompt=None):
        if prompt:
            print(prompt, end="")
        if inputs:
            input_value = inputs.pop(0)
            print(input_value)
            return input_value
        else:
            return 0

    custom_globals = {"input": input_func, "_source_code": code, "__name__": "__main__"}

    # Hae testikoodi tietokannasta, jos mahdollista
    test_code = None
    if task:
        task_test_instance = TaskTest.objects.filter(task=task).first()
        if task_test_instance:
            test_code = task_test_instance.test_code

    def exec_code():
        new_stdout = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = new_stdout
        try:
            exec(code, custom_globals)
            if test_code:
                exec(test_code, custom_globals)
                test_result = custom_globals.get("test_function", lambda x: (True, ""))(custom_globals)
                if not test_result[0]:
                    raise Exception("TestFailed:\n" + test_result[1])
        except Exception as e:
            sys.stdout = old_stdout
            return {"error": str(e), "output": ""}
        output = new_stdout.getvalue()
        sys.stdout = old_stdout
        return {"output": output}

    try:
        # Sovelletaan aikakatkaisua kaikkiin suorituksiin
        result = func_timeout(1, exec_code)
    except FunctionTimedOut:
        return JsonResponse({"error": "Timeout error", "output": ""})
    except Exception as e:
        return JsonResponse({"error": str(e), "output": ""})

    # Palautetaan JsonResponse riippuen suorituksen tuloksesta
    if "error" in result:
        return JsonResponse({"error": result["error"], "output": ""})
    else:
        return JsonResponse({"output": result["output"]})

