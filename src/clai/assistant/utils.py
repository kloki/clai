import subprocess


def run_bash(command, split=True):
    if split:
        command = command.split(" ")
    return (
        subprocess.Popen(command, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
    )
