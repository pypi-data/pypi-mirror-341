import argparse
import os
import subprocess
from colorama import Fore, Back, Style, init as colorama_init

def print_cmd(cmd):
    print(Fore.YELLOW + " ".join(cmd) + Fore.RESET)

def main():
    colorama_init()
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action='store_true')
    parser.add_argument("name")
    args = parser.parse_args()

    if args.build:
        cmd = ['python', 'setup.py', 'bdist_wheel']
        print_cmd(cmd)
        subprocess.run(cmd)

    cmd = ['pip', 'uninstall', args.name, '-y']
    print_cmd(cmd)
    subprocess.run(cmd)
    cd = os.getcwd()
    
    paths = [os.path.join('dist', n) for n in os.listdir('dist')]
    items = [(path, os.path.getmtime(path)) for path in paths]

    items.sort(key=lambda item: item[1])
    path = items[-1][0]
    
    cmd = ['pip', 'install', path]
    print_cmd(cmd)
    subprocess.run(cmd)

if __name__ == "__main__":
    main()