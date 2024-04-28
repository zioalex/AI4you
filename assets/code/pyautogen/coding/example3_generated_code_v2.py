import subprocess
import hashlib
import os

def get_installed_packages():
    return subprocess.check_output(['dpkg', '--list']).decode().splitlines()

def get_file_info(package_name, file_name):
    output = subprocess.check_output(['apt-file', 'ls', package_name]).decode()
    lines = [line.strip() for line in output.split('\n') if line]
    file_info = None
    for line in lines:
        if file_name in line:
            parts = line.split('/')
            file_info = {'package': package_name, 'file': file_name,
                          'current_size': os.path.getsize(os.path.join('/var/lib/dpkg/', parts[-1])),
                          'modification_time': str(int(os.path.getmtime(os.path.join('/var/lib/dpkg/', parts[-1])))))
    return file_info

def compare_md5sum(package_name, file_name):
    md5sum = subprocess.check_output(['dpkg', '-s', package_name, file_name]).decode().split(':')[1].strip()
    expected_size = int(md5sum)
    actual_size = os.path.getsize(os.path.join('/var/lib/dpkg/', file_name))
    return (expected_size != actual_size), expected_size, actual_size

def report_differences(package_name):
    for package in get_installed_packages():
        if 'package:' not in package:
            continue
        parts = package.split(': ')
        package_name_parts = parts[1].split()
        if len(package_name_parts) > 1 and package_name_parts[0] == package_name:
            package_info = None
            for file in ['README', 'LICENSE']:
                file_info = get_file_info(package_name, file)
                if file_info:
                    size_diff, expected_size, actual_size = compare_md5sum(package_name, file_info['file'])
                    if size_diff:
                        print(f"Package: {package_name}, File: {file_info['file']}, Current size: {actual_size}, New size: {expected_size}, Modification time: {file_info['modification_time']}")
            if not size_diff:
                print(f"No differences found for package: {package_name}")

def main():
    if len(sys.argv) > 1:
        report_differences(sys.argv[1])
    else:
        for package in get_installed_packages():
            if 'package:' not in package:
                continue
            parts = package.split(': ')
            package_name = parts[1].strip()
            print(f"Checking package: {package_name}")
            report_differences(package_name)
            print()

if __name__ == "__main__":
    main()
