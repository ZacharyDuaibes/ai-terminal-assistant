#!/usr/bin/env python3

# Required libraries
import os 
import sys
import sqlite3
import subprocess
from openai import OpenAI

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct absolute path to keys.txt
KEYS_FILE = os.path.join(SCRIPT_DIR, 'keys.txt')
# Load and read my OpenAI API key file
with open(KEYS_FILE, 'r') as file:
    KEY = file.read().strip() 

# Constants for file paths (all in home directory)
# Log commands in home directory
LOG_FILE = os.path.expanduser("~/commands.txt")
# Flag file to enable toggle
FLAG_FILE = os.path.expanduser("~/.logging_flag")
# DB file
DB_FILE = os.path.expanduser("~/commands.db")

# Storing most recent command
LAST_COMMAND = ""

# Using 'preexec()' to store the most recent command
# 'preexec()' is executed after you press enter but before it is executed 
def preexec(command):
    global LAST_COMMAND
    LAST_COMMAND = command

# Grabs the exit staus of a command using 'os.system()'
def check_command_hook(LAST_COMMAND):
    result = subprocess.run(LAST_COMMAND, shell=True, capture_output=True, text=True)
    return result.returncode

# Enable/disable logging based on state ('1' to start, '0' to end)
def toggle_logging(state):
    if state == "1":
        open(FLAG_FILE, "w").close()
        print("Logging on")
    elif state == "0":
        if os.path.exists(FLAG_FILE):
            os.remove(FLAG_FILE)
        print("Logging off")

# Generate a description of what a command does using OpenAI's API
# Takes a command string as input and returns a natural language description
def generate_command_description(command):
   client = OpenAI(api_key=KEY)
   prompt = f"Provide a concise description of what the following command does:\n\n{command}"
   response = client.chat.completions.create(
       model = "gpt-3.5-turbo",
       messages = [
           {"role": "system", "content": "You are an expert command interpreter for any operating system."},
           {"role": "user", "content": prompt}
       ],
       temperature = 0.5
   )
   description = response.choices[0].message.content.strip()
   return description

def main():
    # Require at least one argument
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
            connect = sqlite3.connect(DB_FILE)
            cursor = connect.cursor()
            
            try:
                # Find executed command in database 
                cursor.execute('''
                    SELECT command_text FROM commands WHERE command_text = ?
                ''', (LAST_COMMAND,))
                row = cursor.fetchone()

                # If command found in database, only update usage counter
                if row:
                    cursor.execute('''
                        UPDATE commands 
                        SET usage_count = usage_count + 1,
                            last_used = CURRENT_TIMESTAMP
                        WHERE command_text = ?
                    ''', (LAST_COMMAND,))
                    connect.commit()
                
                # If command not found in database, add it and make the API call
                else:
                    description = generate_command_description(LAST_COMMAND)
                    cursor.execute('''
                        INSERT INTO commands (command_text, description, first_used, last_used, usage_count)
                        VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
                    ''', (LAST_COMMAND, description))
                    connect.commit()

            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"API or other error: {e}")
            finally:
                connect.close()
    sys.exit(0)

if __name__ == "__main__":
    main()