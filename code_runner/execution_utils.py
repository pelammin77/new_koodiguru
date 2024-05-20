import io
import sys
from func_timeout import func_timeout, FunctionTimedOut

def execute_code(code, inputs=[], language="python", test_code=None):
    # Oletetaan, että tämä funktio suorittaa koodin perustuen annettuun kieleen
    # Tässä esimerkissä käsitellään vain Pythonia
    if language == "python":
        return execute_python_code(code, inputs, test_code)
    elif language == "c":
        return execute_c_code(code, inputs, test_code)
    elif language == "cpp":
        return execute_cpp_code(code, inputs, test_code)
    else:
        return {"error": "Unsupported language specified", "output": ""}





def execute_python_code(code, inputs=[], test_code=None):
    """
    Suorittaa koodin ja valinnaisen testikoodin.
    
    :param code: Suoritettava Python-koodi.
    :param inputs: Lista syötteistä, jotka välitetään koodille.
    :param test_code: Python-koodi, joka sisältää testit.
    :return: Sanakirja, joka sisältää suorituksen tuloksen tai virheen.
    """
    def input_func(prompt=None):
        if inputs:
            return inputs.pop(0)
        return ''

    custom_globals = {'input': input_func}
    
    result = {'output': '', 'error': '', 'test_results': None}
    
    # Uudelleenohjaa stdout
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    try:
        # Aseta aikakatkaisu ja suorita koodi
        exec_code = compile(code, '<string>', 'exec')
        func_timeout(2, exec, args=(exec_code, custom_globals))
        
        # Suorita testikoodi, jos se on annettu
       # print(f"test_code arvo: {test_code}")
      #  print(f"Code: {code}")
        if test_code:
            print("testi koodi löytyi testi suoritetaan")
            exec_test_code = compile(test_code, '<string>', 'exec')
            func_timeout(5, exec, args=(exec_test_code, custom_globals))
            # Oleta, että testikoodi asettaa tulokset globaliin muuttujaan
            result['test_results'] = custom_globals.get('test_results')
            if 'test_results' in custom_globals and not custom_globals['test_results'][0]:
                # Testi epäonnistui
                result['error'] = 'TestFailed: ' + custom_globals['test_results'][1]
     
     
        result['output'] = new_stdout.getvalue()
    except FunctionTimedOut:
        result['error'] = 'Timeout: Koodin suoritus kesti liian kauan.'
    except Exception as e:
        result['error'] = str(e)
    finally:
        # Palauta stdout normaaliksi
        sys.stdout = old_stdout

    return result

def execute_c_code(code, inputs=[], task_id=None, test_code=None):
    pass

def execute_cpp_code(code, inputs=[], task_id=None, test_code=None):
    pass