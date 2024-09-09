# filename: coding/example3_generated_code-v6.py
import subprocess
import os
import sys
import hashlib

def get_installed_packages():
    output = subprocess.check_output(["dpkg", "--get-selections"]).decode("utf-8").split("\n")
    return [line.split()[0] for line in output if line]

def get_file_info(package_name):
    output = subprocess.check_output(["dpkg", "-L", package_name]).decode("utf-8").split("\n")
    return [line for line in output if line and not line.strip().startswith('/.')]

def check_file_integrity(package_name):
    files = get_file_info(package_name)
    for file in files:
        file_path = file
        if os.path.isfile(file):
            try:
                file_size = os.path.getsize(file)
                with open(file, 'rb') as f:
                    md5sum = hashlib.md5(f.read()).hexdigest()
                yield (package_name, file, file_size, os.path.getmtime(file), md5sum)
            except FileNotFoundError:
                pass

def main():
    if len(sys.argv) == 1:
        packages = get_installed_packages()
    else:
        packages = [sys.argv[1]]
    for package_name in packages:
        differences = list(check_file_integrity(package_name))
        if differences:
            for diff in differences:
                print(f"Package: {diff[0]}, File: {diff[1]}, Actual size: {diff[2]}, Modification time: {diff[3]}, MD5sum: {diff[4]}")
        else:
            print(f"No differences found for package {package_name}")

if __name__ == "__main__":
    main()