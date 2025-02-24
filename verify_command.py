#!/usr/bin/env python3
import os 
import sys

# Using 'preexec()' to store the most recent command
# 'preexec()' is executed after you press enter but before it is executed 
LAST_COMMAND = ""
def preexec(command):
    global LAST_COMMAND
    LAST_COMMAND = command
    return LAST_COMMAND

# Grabs the exit staus of a command using 'os.system()'
def check_command_hook(LAST_COMMAND):
    exit_status = os.system(LAST_COMMAND)
    print(f"Exit Satus of '{LAST_COMMAND}'", exit_status)
    return exit_status

def main():
    # Ensure a command argument is provided
    if len(sys.argv) < 2:
        print("Need Command.")
        sys.exit(1) 

    # Construct the full command string from arguments
    full_command = " ".join(sys.argv[1:])
    preexec(full_command)
    # Writes to a file if command is valid
    if check_command_hook(LAST_COMMAND) == 0:
        with open("/usr/local/bin/commands.txt", "a") as file:
            file.write(f"{LAST_COMMAND}\n")
    sys.exit(0) 
    

if __name__ == "__main__":
    main()
