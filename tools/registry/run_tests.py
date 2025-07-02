import subprocess
import threading

def run(*args, **kwargs):
    output = []
    timeout_seconds = 30

    process = subprocess.Popen(
        ["pytest", "tests/test_agent.py", "--maxfail=3", "--disable-warnings"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    def kill_process():
        try:
            process.kill()
            output.append("\nTimeout reached — process was killed.\n")
        except Exception:
            pass

    timer = threading.Timer(timeout_seconds, kill_process)
    timer.start()

    try:
        for line in process.stdout:
            print(line, end="")
            output.append(line)
    finally:
        timer.cancel()

    return "".join(output)
