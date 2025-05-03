# lambda_function.py

import json
import sys
from io import StringIO
import signal
from contextlib import contextmanager
import traceback
from RestrictedPython import compile_restricted, safe_globals
import math
import random
import numpy as np
import time

class TimeoutError(Exception):
    pass

@contextmanager
def timeout(seconds):
    def signal_handler(signum, frame):
        raise TimeoutError("Code execution timed out")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

class RestrictedExecutor:
    def __init__(self, debug=False):
        self.debug = debug
        self.stdout = StringIO()

        self.allowed_modules = {
            'math': {'sin', 'cos', 'tan', 'pi', 'sqrt', 'floor', 'ceil', 'radians', 'degrees', 'pow', 'fabs'},
            'random': {'random', 'randint', 'choice', 'randrange', 'shuffle'}
        }

    def _write(self, text):
        print(text, file=self.stdout, end='')

    def get_print(self):
        def print_function(*args, **kwargs):
            end = kwargs.get('end', '\n')
            sep = kwargs.get('sep', ' ')
            self._write(sep.join(str(arg) for arg in args) + end)
        return print_function

    def get_restricted_globals(self):
        g = dict(safe_globals.copy())

        g['print'] = self.get_print()
        g['input'] = lambda prompt="": ""

        g['Exception'] = Exception
        g['BaseException'] = BaseException

        g['math'] = {name: getattr(math, name) for name in self.allowed_modules['math'] if hasattr(math, name)}
        g['random'] = {name: getattr(random, name) for name in self.allowed_modules['random'] if hasattr(random, name)}
        g['np'] = np

        return g

    def execute(self, code, inputs=None, test_code=None):
        self.stdout = StringIO()
        if inputs is None:
            inputs = []

        input_iter = iter(inputs)
        def restricted_input(prompt=""):
            try:
                val = next(input_iter)
                self._write(prompt + str(val) + '\n')
                return val
            except StopIteration:
                return ""

        try:
            globals_ = self.get_restricted_globals()
            globals_['input'] = restricted_input
            globals_['_source_code'] = code

            byte_code = compile_restricted(code, '<inline>', 'exec')
            with timeout(3):
                exec(byte_code, globals_)
                output = self.stdout.getvalue()

                # Save output lines for test_function
                globals_['_printed_output'] = output.splitlines()

                if test_code:
                    if self.debug:
                        self._write("\nExecuting test code...\n")
                    test_byte_code = compile_restricted(test_code, '<test>', 'exec')
                    exec(test_byte_code, globals_)
                    test_function = globals_.get("test_function")
                    if test_function:
                        test_result = test_function(globals_)
                        if not test_result[0]:
                            raise Exception("TestFailed:\n" + test_result[1])

            return {"output": output, "error": None}

        except TimeoutError:
            return {"error": "Timeout error: Code execution took too long", "output": self.stdout.getvalue()}
        except Exception as e:
            msg = str(e)
            if self.debug:
                msg += "\n" + traceback.format_exc()
            return {"error": msg, "output": self.stdout.getvalue()}

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        code = body.get('code', '')
        inputs = body.get('inputs', [])
        test_code = body.get('test_code')
        debug = body.get('debug', False)
        user_id = body.get('user_id')
        task_id = body.get('task_id')

        executor = RestrictedExecutor(debug=debug)
        result = executor.execute(code, inputs, test_code)

        result['usage_metrics'] = {
            'user_id': user_id,
            'task_id': task_id,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        if debug:
            result['debug_info'] = {
                'received_code': code,
                'received_inputs': inputs,
                'has_test_code': bool(test_code),
                'allowed_modules': executor.allowed_modules
            }

        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        error = {
            'error': str(e),
            'output': '',
            'usage_metrics': {
                'user_id': body.get('user_id') if 'body' in locals() else None,
                'task_id': body.get('task_id') if 'body' in locals() else None,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        if debug:
            error['debug_info'] = {'traceback': traceback.format_exc()}
        return {
            'statusCode': 500,
            'body': json.dumps(error),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
