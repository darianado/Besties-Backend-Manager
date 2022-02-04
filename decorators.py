import time

def sleepy_exit(function):
    def sleeping(seconds: float):
        partitions = 3

        for _ in range(partitions):
            print(".", end="", flush=True)
            time.sleep(seconds / partitions)
        print("")

    def sleepy_function():
        function()
        time.sleep(1)
        
    return sleepy_function

def safe_exit(function):
    def safe_function():
        try:
            function()
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    return safe_function