import os
import subprocess
import sys

# Set the Flask app
os.environ["FLASK_APP"] = "en_cavale/__init__.py"

# Start Flask shell
process = subprocess.Popen(
    [sys.executable, "-m", "flask", "shell"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

# Command to run in Flask shell
command = "from en_cavale.spending.spending import start; start()\n"

# Send the command to the Flask shell
stdout, stderr = process.communicate(input=command)

# Print output
print(stdout)
print(stderr, file=sys.stderr)
