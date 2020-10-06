import os
import argparse
import re

# Constants
FILE_PATH = './version.cfg'
DEFAULT_VERSION = '0.0.0-dev'
VERSION_REGEX = r'(\d+).(\d+).(\d+)'

def check_file_exists(path: str) -> bool:
    return os.path.isfile(path)

def create_version_file(path: str):
    with open(path, 'w') as f:
        f.write(DEFAULT_VERSION)   

def load() -> str:
    # check if version file exists
    if check_file_exists(FILE_PATH) is False:
        create_version_file(FILE_PATH)
    with open(FILE_PATH, 'r') as vf:
        return vf.readline()

def save(version: str = DEFAULT_VERSION):
    with open(FILE_PATH, 'w') as f:
        f.write(version)

def increase_version(major: bool = False, minor: bool = False, patch: bool = False, dev: bool = False) -> str:
    # match version regex
    p = re.compile(VERSION_REGEX, re.IGNORECASE)
    groups = p.match(load()).groups()
    
    # increase version
    v_major = groups[0] if major is False else int(groups[0]) + 1
    v_minor = groups[1] if minor is False else int(groups[1]) + 1
    v_patch = groups[2] if patch is False else int(groups[2]) + 1
    v_dev = '' if dev is False else '-dev'

    v_string = f'{v_major}.{v_minor}.{v_patch}{v_dev}'
    return v_string


if __name__ == "__main__":
    # parse input args
    parser = argparse.ArgumentParser(description='Autoversion utility. Automatize semantic versioning (https://semver.org/).')
    parser.add_argument('-M', '--major', action='store_true', help='Increase major version')
    parser.add_argument('-m', '--minor', action='store_true', help='Increase minor version')
    parser.add_argument('-p', '--patch', action='store_true', help='Increase patch version')
    parser.add_argument('-d', '--dev', action='store_true', help='Development version')
    args = parser.parse_args()

    # increase version accordingly to args
    next_version = increase_version(args.major, args.minor, args.patch, args.dev)
    print(next_version)

    # update version file
    save(next_version)