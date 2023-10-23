import subprocess
import os

# Prompt the user for the container name
container = input("Enter the name of the container: ")

# Check if the script is running as root (sudo)
if os.geteuid() != 0:
    print("Please run the script with sudo to ensure proper permissions.")
    exit(1)

# Run the 'podman inspect' command to get the container information
inspect_command = ["podman", "inspect", "--format", "{{.GraphDriver.Data.UpperDir}}", container]
process = subprocess.Popen(inspect_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

stdout, stderr = process.communicate()

if process.returncode == 0:
    upper_dir = stdout.strip()
    try:
        # Use the 'du' command to estimate the container size
        du_command = ["du", "-sh", upper_dir]
        process = subprocess.Popen(du_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            size_info = stdout.split()[0]
            print(f"Container {container} size: {size_info}")
        else:
            print(f"Error estimating container size: {stderr}")
    except Exception as e:
        print(f"Error estimating container size: {str(e)}")
else:
    print(f"Error: {stderr}")

