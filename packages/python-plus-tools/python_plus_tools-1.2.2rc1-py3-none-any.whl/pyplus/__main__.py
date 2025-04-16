import argparse
from sys import prefix, exit
import pyplus

# print(prefix + "\\python.exe: No module named pyplus.__main__; 'pyplus' is a package and cannot be directly executed")

# exit(-1)

parser = argparse.ArgumentParser(description="imgfit commands")
subparsers = parser.add_subparsers(dest="command", required=True)

config_cmd = subparsers.add_parser("config", help="Set the config setting.")
config_cmd.add_subparsers(dest="namespace", required=True)
subparsers.add_parser("version", help="Get the pyplus version.")

args = parser.parse_args()

if args.command == "config":
    pass
elif args.command == "version":
    print("Version : pyplus",pyplus.get_pre_version())
