#!/usr/bin/env python3

# Required libraries
import os 
import sys

# Log commands in home directory
LOG_FILE = os.path.expanduser("~/commands.txt")
# Flag file to enable toggle
FLAG_FILE = os.path.expanduser("~/.logging_flag")

# Storing most recent command
LAST_COMMAND = ""

# Using 'preexec()' to store the most recent command
# 'preexec()' is executed after you press enter but before it is executed 
def preexec(command):
    global LAST_COMMAND
    LAST_COMMAND = command

# Grabs the exit staus of a command using 'os.system()'
def check_command_hook(LAST_COMMAND):
    exit_status = os.system(LAST_COMMAND)
    print(f"Exit Satus of '{LAST_COMMAND}'", exit_status)
    return exit_status

def toggle_logging(state):
    if state == "1":
        open(FLAG_FILE, "w").close()
        print("Logging on")
    elif state == "0":
        if os.path.exists(FLAG_FILE):
            os.remove(FLAG_FILE)
        print("Logging off")

def main():
    # Require at least one argument.
    if len(sys.argv) < 2:
        print("Usage: verify_command.py [1|0|<command>]")
        sys.exit(1)
    
    # If the first argument is "1" or "0", call toggle_logging
    if sys.argv[1] in ["1", "0"]:
        toggle_logging(sys.argv[1])
        sys.exit(0)
    
    # Otherwise, treat the arguments as the command to verify.
    full_command = " ".join(sys.argv[1:])
    preexec(full_command)
    
    # Only proceed if logging is enabled (i.e. the flag file exists).
    if os.path.exists(FLAG_FILE):
        if check_command_hook(LAST_COMMAND) == 0:
            with open(LOG_FILE, "a") as file:
                file.write(f"{LAST_COMMAND}\n")
    else:
        # Logging is disabled; do nothing or simply exit.
        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
