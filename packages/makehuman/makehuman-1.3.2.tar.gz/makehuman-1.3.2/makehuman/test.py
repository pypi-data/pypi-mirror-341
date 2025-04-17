def hello():
    print("Hello, world!")
    
import subprocess
import os

def start_app():
    # Get the path to the makehuman.py file
    makehuman_path = os.path.join(os.path.dirname(__file__), "makehuman.py")

    # Run the makehuman.py file
    subprocess.run(["python.exe", makehuman_path])