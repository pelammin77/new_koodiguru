# lambda_function.py

import json
import sys
from io import StringIO
import signal
from contextlib import contextmanager
import traceback
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins, guarded_iter_unpack_sequence
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
        
        # Define allowed modules with specific functions
        self.allowed_modules = {
            'math': {
                'sin', 'cos', 'tan', 'pi', 'sqrt', 'floor', 'ceil',
                'radians', 'degrees', 'pow', 'fabs'
            },
            'random': {
                'random', 'randint', 'choice', 'randrange', 'shuffle'
            }
        }

    def _write(self, text):
        """Write to stdout buffer"""
        print(text, file=self.stdout, end='')
        
    def get_print(self):
        """Create a safe print function"""
        def print_function(*args, **kwargs):
            end = kwargs.get('end', '\n')
            sep = kwargs.get('sep', ' ')
            self._write(sep.join(str(arg) for arg in args) + end)
        return print_function

    def get_restricted_globals(self):
        """Create restricted globals dictionary with allowed functions"""
        restricted_globals = {
            '__builtins__': {
                # Basic operations
                'abs': abs, 'bool': bool, 'int': int, 'float': float, 'str': str,
                'len': len, 'max': max, 'min': min, 'sum': sum, 'round': round,
                
                # Container types
                'list': list, 'dict': dict, 'set': set, 'tuple': tuple,
                
                # Iteration
                'range': range, 'enumerate': enumerate, 'zip': zip,
                'iter': iter, 'next': next,
                
                # String operations
                'chr': chr, 'ord': ord,
                
                # Type checking
                'isinstance': isinstance, 'type': type,
                
                # Safe operations
                'sorted': sorted,
                'reversed': reversed,
                'all': all,
                'any': any,
            },
            '_getiter_': iter,
            '_iter_unpack_sequence_': guarded_iter_unpack_sequence,
            'print': self.get_print(),
        }

        # Add math functions
        math_funcs = {}
        for func_name in self.allowed_modules['math']:
            if hasattr(math, func_name):
                math_funcs[func_name] = getattr(math, func_name)
        restricted_globals['math'] = math_funcs

        # Add random functions
        random_funcs = {}
        for func_name in self.allowed_modules['random']:
            if hasattr(random, func_name):
                random_funcs[func_name] = getattr(random, func_name)
        restricted_globals['random'] = random_funcs

        # Add numpy module directly
        restricted_globals['np'] = np

        return restricted_globals

    def execute(self, code, inputs=None, test_code=None):
        """Execute code in restricted environment"""
        if inputs is None:
            inputs = []
            
        input_iterator = iter(inputs)
        
        def restricted_input(prompt=""):
            try:
                value = next(input_iterator)
                self._write(prompt + str(value) + '\n')
                return value
            except StopIteration:
                return ""

        try:
            # Prepare restricted environment
            restricted_globals = self.get_restricted_globals()
            restricted_globals['input'] = restricted_input
            restricted_globals['_source_code'] = code

            # Compile restricted code
            byte_code = compile_restricted(
                code,
                '<inline>',
                'exec',
                policy=None
            )

            # Execute code with timeout
            with timeout(3):  # 3 second timeout
                exec(byte_code, restricted_globals)
                output = self.stdout.getvalue()

                # Execute test code if provided
                if test_code:
                    if self.debug:
                        self._write("\nExecuting test code...\n")
                        
                    test_byte_code = compile_restricted(
                        test_code,
                        '<test>',
                        'exec',
                        policy=None
                    )
                    exec(test_byte_code, restricted_globals)
                    
                    test_function = restricted_globals.get("test_function")
                    if test_function:
                        test_result = test_function(restricted_globals)
                        if not test_result[0]:
                            raise Exception("TestFailed:\n" + test_result[1])

            return {
                "output": output,
                "error": None
            }

        except TimeoutError:
            return {
                "error": "Timeout error: Code execution took too long",
                "output": self.stdout.getvalue()
            }
        except Exception as e:
            error_msg = str(e)
            if self.debug:
                error_msg += f"\nTraceback: {traceback.format_exc()}"
            return {
                "error": error_msg,
                "output": self.stdout.getvalue()
            }

def lambda_handler(event, context):
    """AWS Lambda handler function"""
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        code = body.get('code', '')
        inputs = body.get('inputs', [])
        test_code = body.get('test_code')
        debug_mode = body.get('debug', False)
        user_id = body.get('user_id')
        task_id = body.get('task_id')

        if debug_mode:
            print(f"Received code: {code}")
            print(f"Received inputs: {inputs}")
            print(f"Test code: {test_code}")

        # Execute code
        executor = RestrictedExecutor(debug=debug_mode)
        result = executor.execute(code, inputs, test_code)

        # Add usage metrics to result
        result['usage_metrics'] = {
            'user_id': user_id,
            'task_id': task_id,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        # Add debug information if requested
        if debug_mode:
            result['debug_info'] = {
                'received_code': code,
                'received_inputs': inputs,
                'has_test_code': bool(test_code),
                'allowed_modules': executor.allowed_modules
            }

        # Return response
        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        error_info = {
            'error': str(e),
            'output': '',
            'usage_metrics': {
                'user_id': body.get('user_id') if 'body' in locals() else None,
                'task_id': body.get('task_id') if 'body' in locals() else None,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        if debug_mode:
            error_info['debug_info'] = {
                'traceback': traceback.format_exc()
            }
        return {
            'statusCode': 500,
            'body': json.dumps(error_info),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }