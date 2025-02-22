import os
import subprocess
import sys

# Check if a given command is valid
def is_valid_command(command):
    # Extract the main command (first word) from the input
    cmd = command.split()[0] if command.split() else ""

    # Return False if the command is empty
    if not cmd: 
        return False

    try:
        # Check if the command exists using 'command -v'
        result = subprocess.run(
            ["command", "-v", cmd],  # Runs 'command -v <cmd>' to check existence
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Return True if output is not empty, indicating command exists
        return bool(result.stdout.strip())
    except Exception:
        return False  # If an error occurs, assume the command is invalid

# Handle command-line input and validation
def main():
    # Ensure a command argument is provided
    if len(sys.argv) < 2:
        print("Usage: verify_command.py <command>")
        sys.exit(1) 

    # Construct the full command string from arguments
    full_command = " ".join(sys.argv[1:])

    # Check if the command is valid and print the appropriate message
    if is_valid_command(full_command):
        print(f"'{full_command}' is a valid command.")
        sys.exit(0) 
    else:
        print(f"'{full_command}' is not a valid command.")
        sys.exit(1) 

if __name__ == "__main__":
    main()
