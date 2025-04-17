import subprocess

def run_command(cmd, timeout=None):
    """
    Execute a shell command and return its output.
    """
    result = subprocess.run(
        cmd, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout
    )
    return result.stdout + result.stderr