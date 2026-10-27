import modal

app = modal.App("opsaegis-runner")
image = modal.Image.debian_slim()

@app.function(image=image)
def execute_remediation(remediation_cmd: str, verification_cmd: str):
    import subprocess
    import sys
    import time

    # 1. Suntikkan failure nyata: buat file script dan jalankan di background
    leak_script = "/tmp/leak_simulator.py"
    with open(leak_script, "w") as f:
        f.write("import time\ntime.sleep(300)\n")

    # Jalankan proses menggunakan path interpreter Python aktif
    subprocess.Popen([sys.executable, leak_script])
    time.sleep(1)

    # 2. Eksekusi script perbaikan dari model
    fix_proc = subprocess.run(
        remediation_cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    # 3. Eksekusi perintah verifikasi
    verify_proc = subprocess.run(
        verification_cmd,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "exit_code": verify_proc.returncode,
        "fix_stdout": fix_proc.stdout,
        "fix_stderr": fix_proc.stderr,
        "verify_stdout": verify_proc.stdout,
        "verify_stderr": verify_proc.stderr
    }