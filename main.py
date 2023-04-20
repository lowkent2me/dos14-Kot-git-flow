import os

shell_name = os.environ["SHELL"]
if shell_name == "/bin/bash":
    print("Greetings BASH")
else:
    print("Hello " + shell_name[5:])
