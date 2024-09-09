# filename: coding/example3_generated_code-v2.py
import os
import hashlib
import gzip
import shutil
import subprocess

# Function to get the installed packages
def get_installed_packages():
    output = subprocess.check_output(["dpkg", "--get-selections"]).decode("utf-8")
    return [line.split()[0] for line in output.splitlines()]

# Function to get the files of a package
def get_package_files(package):
    output = subprocess.check_output(["dpkg", "-L", package]).decode("utf-8")
    return [line.strip() for line in output.splitlines()]

# Function to get the md5sum of a file in the dpkg database
def get_file_md5sum(package, file):
    output = subprocess.check_output(["dpkg", "--verify", package]).decode("utf-8")
    for line in output.splitlines():
        if file in line:
            return line.split()[0]
    return None

# Function to calculate the md5sum of a file
def calculate_md5sum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to check the md5sum of a file
def check_md5sum(file_path, expected_md5sum):
    actual_md5sum = calculate_md5sum(file_path)
    return actual_md5sum == expected_md5sum

# Function to log inaccessible files
def log_inaccessible_file(file_path, file_size, modification_time):
    print(f"Warning: Unable to access file {file_path} ({file_size} bytes, modified {modification_time})")

# Main function
def main(package=None):
    output_file = "output.log"
    with open(output_file, "w") as f:
        if package:
            packages = [package]
        else:
            packages = get_installed_packages()
        
        for package in packages:
            print(f"Checking package {package}")
            f.write(f"Checking package {package}\n")
            files = get_package_files(package)
            for file in files:
                file_path = os.path.join("/", file)
                try:
                    file_size = os.path.getsize(file_path)
                    modification_time = os.path.getmtime(file_path)
                    print(f"Checking file {file_path} ({file_size} bytes, modified {modification_time})")
                    f.write(f"Checking file {file_path} ({file_size} bytes, modified {modification_time})\n")
                    expected_md5sum = get_file_md5sum(package, file)
                    if expected_md5sum:
                        if check_md5sum(file_path, expected_md5sum):
                            print(f"md5sum matches for file {file_path}")
                            f.write(f"md5sum matches for file {file_path}\n")
                        else:
                            print(f"md5sum mismatch for file {file_path}")
                            f.write(f"md5sum mismatch for file {file_path}\n")
                    else:
                        print(f"md5sum not found for file {file_path} in dpkg database")
                        f.write(f"md5sum not found for file {file_path} in dpkg database\n")
                except Exception as e:
                    log_inaccessible_file(file_path, file_size, modification_time)
                    f.write(f"Warning: Unable to access file {file_path} ({file_size} bytes, modified {modification_time})\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()