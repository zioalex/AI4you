# filename: example3_generated_code.py
import os
import hashlib
import subprocess
import sys



def get_installed_packages():
    command = "dpkg --list | awk '{print $1}'"
    output = subprocess.check_output(command, shell=True).decode("utf-8").splitlines()
    return [line.strip() for line in output]

def get_package_file_list(package):
    if package:
        command = f"dpkg -L {package}"
    else:
        command = "dpkg -L"
    output = subprocess.check_output(command, shell=True).decode("utf-8").splitlines()
    return [line.strip() for line in output]

def get_file_properties(file_path):
    stat_info = os.stat(file_path)
    file_size = str(stat_info.st_size)
    modification_time = str(stat_info.st_mtime)
    return file_size, modification_time

def check_md5sum(package):
    if package:
        command = f"dpkg --query -L {package} | xargs md5sum"
    else:
        command = "dpkg --query -L | xargs md5sum"
    output = subprocess.check_output(command, shell=True).decode("utf-8").splitlines()
    return [line.split()[1].strip() for line in output]

def main(package=None):
    installed_packages = get_installed_packages()
    package_file_list = []
    if package:
        package_file_list = get_package_file_list(package)
    else:
        for package_name in installed_packages:
            package_file_list.extend(get_package_file_list(package_name))

    differences = {}
    for file_path in package_file_list:
        original_md5sum = check_md5sum(None)[package_file_list.index(file_path)]
        stat_info = os.stat(file_path)
        file_size, modification_time = get_file_properties(file_path)

        if (file_size != str(os.path.getsize(file_path)) or
            modification_time != str(stat_info.st_mtime)):
            differences[file_path] = {
                "package": package_name if package else None,
                "original_md5sum": original_md5sum,
                "current_size": file_size,
                "new_size": str(os.path.getsize(file_path)),
                "modification_time": modification_time
            }

    for file_path, properties in differences.items():
        print("Package:", properties["package"] if properties["package"] else None)
        print("File name:", file_path)
        print("Original size:", properties["original_md5sum"])
        print("Current size:", properties["current_size"])
        print("New size:", properties["new_size"])
        print("Modification time:", properties["modification_time"])

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)

print("TERMINATE")
