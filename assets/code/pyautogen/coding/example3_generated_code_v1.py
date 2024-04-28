import os
import hashlib
import subprocess

def get_installed_packages():
    packages = []
    output = subprocess.check_output([ 'dpkg', '--list' ])
    for line in output.decode('utf-8').splitlines():
        if len(line) > 1:
            parts = line.split()
            package_name = parts[0].decode().strip()
            packages.append(package_name)
    return packages

def get_package_files(package_name):
    files = []
    output = subprocess.check_output(['dpkg', '--listfiles', package_name])
    for line in output.decode('utf-8').splitlines():
        file_path, file_size = line.split()
        if os.path.isfile(file_path):
            files.append((package_name, file_path, int(file_size)))
    return files

def compare_md5sums(package_name, file_path):
    original_file_size = 0
    md5sum_command = f'apt-get --print-md5sums {package_name} {file_path}'
    try:
        output = subprocess.check_output(md5sum_command, shell=True)
        _, original_md5sum = output.decode('utf-8').split()
    except subprocess.CalledProcessError:
        return None
    new_file_size = os.path.getsize(file_path)
    md5sum = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    return package_name, file_path, original_file_size, new_file_size, os.path.getmtime(file_path), original_md5sum != md5sum

def main(package_name=None):
    if not package_name:
        installed_packages = get_installed_packages()
    else:
        installed_packages = [package_name]
    
    for package_name in installed_packages:
        files = get_package_files(package_name)
        for file_info in files:
            result = compare_md5sums(*file_info)
            if result and (result[6] or result[3] != result[4]):
                print(f"Package: {package_name}, File: {result[1]}, Original Size: {result[2]}, New Size: {result[3]}, Modification Time: {result[4]}, Original MD5Sum: {result[5]}")

if __name__ == "__main__":
    main()
