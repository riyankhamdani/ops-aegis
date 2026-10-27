import modal

app = modal.App("opsaegis-runner")
image = modal.Image.debian_slim().run_commands("apt-get update && apt-get install -y procps")

@app.function(image=image)
def execute_remediation(remediation_cmd: str, verification_cmd: str):
    """Mengeksekusi tindakan perbaikan di dalam Modal Sandbox yang terisolasi."""
    import subprocess

    fix_proc = subprocess.run(
        remediation_cmd, shell=True, capture_output=True, text=True
    )
    verify_proc = subprocess.run(
        verification_cmd, shell=True, capture_output=True, text=True
    )
    
    return {
        "fix_stdout": fix_proc.stdout.strip(),
        "fix_stderr": fix_proc.stderr.strip(),
        "verify_stdout": verify_proc.stdout.strip(),
        "exit_code": verify_proc.returncode
    }
