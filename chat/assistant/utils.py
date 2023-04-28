import subprocess


def run_bash(command):
    return (
        subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
        .stdout.read()
        .decode("utf-8")
    )
