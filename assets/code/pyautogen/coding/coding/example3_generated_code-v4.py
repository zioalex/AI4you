# filename: coding/example3_generated_code-v4.py
import os
import hashlib
import gzip
import shutil
import subprocess
import concurrent.futures

# Function to get the installed packages
def get_installed_packages():
    output = subprocess.check_output(["dpkg", "--get-selections"]).decode("utf-8")
    return [line.split()[0] for line in output.splitlines()]

# ... (rest of the code remains the same)

# Main function
def main(package=None):
    if package:
        packages = [package]
    else:
        packages = get_installed_packages()
    
    with open("output.log", "w") as f:
        f.write("")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_package, package): package for package in packages}
        for future in concurrent.futures.as_completed(futures):
            package = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing package {package}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()