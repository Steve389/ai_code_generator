import subprocess
import os

# Install other dependencies
subprocess.check_call(["pip3", "install", "-r", "requirements.txt"])

# Set environment variables
os.environ["CMAKE_ARGS"] = "-DLLAMA_METAL=on"
os.environ["FORCE_CMAKE"] = "1"

# Install llama-cpp-python with no cache
subprocess.check_call(["pip3", "install", "--no-cache-dir", "llama-cpp-python==0.2.58"])
