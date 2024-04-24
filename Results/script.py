import subprocess
import time
import os

print("Results Script")

process1 = subprocess.Popen(["python", "summary.py"])
process2 = subprocess.Popen(["python", "merger.py"])

process1.wait()
process2.wait()


