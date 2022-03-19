import time

from constants import SLEEPY_EXIT_DURATION

def sleepy_exit(function):
    def sleepy_function(*args, **kwargs):
        function(*args, **kwargs)
        time.sleep(SLEEPY_EXIT_DURATION)
        
    return sleepy_function

def safe_exit(function):
    def safe_function(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    return safe_function