import os
import sys
import subprocess


def get_last_command(shell):
    """
    Get the last command from shell history, excluding 'sudoh'.
    """
    home = os.path.expanduser("~")
    if shell.endswith("zsh"):
        histfile = os.path.join(home, ".zsh_history")
        with open(histfile, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        # zsh history lines can have timestamps: ': 1680000000:0;command'
        commands = [l.split(';',1)[-1].strip() for l in lines if ';' in l]
    elif shell.endswith("bash"):
        histfile = os.path.join(home, ".bash_history")
        with open(histfile, "r", encoding="utf-8", errors="ignore") as f:
            commands = [l.strip() for l in f if l.strip()]
    else:
        print("Unsupported shell. Only bash and zsh are supported.")
        sys.exit(1)
    # Exclude 'sudoh' invocations
    for cmd in reversed(commands):
        if not cmd.strip().startswith("sudoh"):
            return cmd
    print("No previous command found.")
    sys.exit(1)

def main():
    shell = os.environ.get("SHELL", "")
    last_cmd = get_last_command(shell)
    sudo_cmd = f"sudo {last_cmd}"
    print(f"Running: {sudo_cmd}")
    # Use the user's shell to run the command
    result = subprocess.run(sudo_cmd, shell=True, executable=shell)
    if result.returncode != 0:
        print(f"[ERROR] Command failed with exit code {result.returncode}")

if __name__ == "__main__":
    main()
