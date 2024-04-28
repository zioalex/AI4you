import os
import subprocess

def get_file_md5(filename):
    try:
        md5 = subprocess.check_output(['md5sum', '--quiet', filename]).decode().strip()
        return md5
    except Exception as e:
        print(f"Error while computing MD5 for '{filename}' - Error Message: {e}")
        return None

def get_file_size(filename):
    try:
        stats = os.stat(filename)
        return stats.st_size
    except Exception as e:
        print(f"Error while getting file size for '{filename}' - Error Message: {e}")
        return None

def get_packages():
    packages = []

    for package in os.listdir('/var/lib/dpkg/info'):
        if not package.endswith('.list'):
            continue
        with open(os.path.join('/var/lib/dpkg/info', package), 'r') as f:
            lines = f.readlines()
            for line in lines[1:]:
                fields = line.split(' ')
                if len(fields) < 3 or not all(char.isalnum() or char == '_' or char == '-' for char in fields[0]):
                    continue
                packages.append((fields[0], os.path.join('/var/lib/dpkg/info', package)))
            f.close()
        break

    return packages

def compare(packages):
    mismatches = []

    for package, package_file in packages:
        files = [file for file in os.listdir(os.path.dirname(package_file)) if not file.endswith('.md5') and (file.startswith('.') or '~' not in file)]
        for file in files:
            fullpath = os.path.join(os.path.dirname(package_file), file)
            new_md5 = get_file_md5(fullpath)
            current_size = get_file_size(os.path.join(package, file)) if os.path.exists(os.path.join(package, file)) else 0
            if new_md5 is not None and new_md5 != get_file_md5(os.path.join(package, file)):
                mismatches.append((package, file, new_md5, current_size))
            elif current_size != (get_file_size(fullpath) if os.path.exists(fullpath) else 0):
                mismatches.append((package, file, current_size, get_file_size(fullpath)))

    return mismatches

def main():
    all_packages = get_packages()
    mismatches = compare(all_packages)

    if len(mismatches) > 0:
        print("Mismatches found:")
        for package, file, md5, size in mismatches:
            print(f"Package '{package}', File '{file}'")
            if md5 is not None and size is not None:
                print(f"Current Size: {size}, New Size: {md5}")
            else:
                print(f"Current Size: {size}, New Size: Unknown")
    else:
        print("No mismatches found.")

if __name__ == "__main__":
    main()