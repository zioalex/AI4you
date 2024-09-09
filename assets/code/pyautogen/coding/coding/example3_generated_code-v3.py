# filename: coding/example3_generated_code-v3.py
import os
import hashlib
import gzip
import shutil
import subprocess
import concurrent.futures

# ... (rest of the code remains the same)

# Function to process a package
def process_package(package):
    files = get_package_files(package)
    for file in files:
        file_path = os.path.join("/", file)
        try:
            file_size = os.path.getsize(file_path)
            modification_time = os.path.getmtime(file_path)
            print(f"Checking file {file_path} ({file_size} bytes, modified {modification_time})")
            with open("output.log", "a") as f:
                f.write(f"Checking file {file_path} ({file_size} bytes, modified {modification_time})\n")
            expected_md5sum = get_file_md5sum(package, file)
            if expected_md5sum:
                if check_md5sum(file_path, expected_md5sum):
                    print(f"md5sum matches for file {file_path}")
                    with open("output.log", "a") as f:
                        f.write(f"md5sum matches for file {file_path}\n")
                else:
                    print(f"md5sum mismatch for file {file_path}")
                    with open("output.log", "a") as f:
                        f.write(f"md5sum mismatch for file {file_path}\n")
            else:
                print(f"md5sum not found for file {file_path} in dpkg database")
                with open("output.log", "a") as f:
                    f.write(f"md5sum not found for file {file_path} in dpkg database\n")
        except Exception as e:
            log_inaccessible_file(file_path, file_size, modification_time)
            with open("output.log", "a") as f:
                f.write(f"Warning: Unable to access file {file_path} ({file_size} bytes, modified {modification_time})\n")

# Main function
def main(package=None):
    if package:
        packages = [package]
    else:
        packages = get_installed_packages()
    
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