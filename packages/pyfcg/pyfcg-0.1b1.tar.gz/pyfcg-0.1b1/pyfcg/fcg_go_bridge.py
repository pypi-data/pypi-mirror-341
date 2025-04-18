####################
# Bridge to FCG Go #
####################

import os
import platform
import time

import wget
import warnings
import subprocess
import atexit
import appdirs

from urllib.error import HTTPError
from pyfcg.routes import *

# Global variables #
####################

platform = platform.system()
server_address = 'localhost'
server_port = 9600
fcg_go_process = None

def init(address=server_address, port=server_port, directory=None, launch=True, fcg_go_version="latest"):
    """Establish a connection with FCG Go, downloading it if necessary."""

    # Setting serv_port and server_address
    global server_port, server_address
    server_address = address
    server_port = port

    if directory is None:
        directory = appdirs.user_data_dir(appname="FCG Go", version=fcg_go_version)

    if launch:
        # Check whether FCG Go is available on the system, if so launch, else download, unzip, launch
        if fcg_go_available(directory):
            if fcg_go_process and not fcg_go_process.poll():
                print('FCG Go has already been launched.')
            else:
                launch_fcg_go(directory, address, server_port)
        else:
            print("FCG Go not yet installed. Proceeding with installation...")
            zipfile = download_fcg_go(directory, version=fcg_go_version)
            if zipfile:
                unzip(zipfile, directory)
            if fcg_go_available(directory):
                launch_fcg_go(directory, address, server_port)
            else:
                print("This version of FCG Go could not be located or downloaded (no file to unzip).")


def download_fcg_go(target_directory=None, url=None, version="latest"):
    """Download FCG Go"""
    # Set url
    if url is None:
        url = 'https://emergent-languages.org/fcg-go/'
        
        # If a version was specified, add it to the url
        if version != "latest":
            url += f'{version}/'
        
        # Get platform-specific zip
        if platform == 'Darwin':
            url += 'fcg-go-macos.zip'
        elif platform == 'Linux':
            warnings.warn("Yet to be tested on Linux.")
            url += 'fcg-go-linux.zip'
        elif platform == 'Windows':
            warnings.warn("Yet to be tested on Windows.")
            url += 'fcg-go-windows.zip'

    # Download
    try:
        # If no target_directory was specified, default to user-specific data dir for this version of FCG Go
        if target_directory is None:
            target_directory = appdirs.user_data_dir(appname="FCG Go", version=version)
        os.makedirs(target_directory, exist_ok=True)

        print('Downloading FCG Go...', end=" ")
        file = wget.download(url, out=target_directory)
        print('Done.')

    except HTTPError as exception:
        os.removedirs(target_directory)
        file = None
        print("HTTPError")

    return file


def fcg_go_available(target_directory):
    """Check whether FCG Go is available on the system."""
    if os.path.exists(target_directory + '/FCG Go.app'):
        return True
    else:
        return None


def unzip(zip_file, target_directory):
    """Unzip zip_file into target_directory"""
    print('Extracting FCG Go...')
    if platform == 'Darwin' or platform == 'Linux':
        os.system(f'unzip "{zip_file}" -d "{target_directory}"')
    elif platform == 'Windows':
        os.system(f'tar -xf "{zip_file}" -d "{target_directory}"')
    print('Done.')
    return target_directory


def launch_fcg_go(directory, address, port):
    """Launch FCG Go"""
    if platform == 'Darwin':
        # os.system("open --background --hide " + directory + r'/FCG\ Go.app' + " --hide --args " + address + " " + str(port))
        fcg_go_path = os.path.join(directory, 'FCG Go.app', 'Contents','MacOS','FCG Go')
    elif platform == 'Linux':
        warnings.warn("Yet to be tested on Linux.")
        fcg_go_path = os.path.join(directory, "FCG Go")
    elif platform == 'Windows':
        warnings.warn("Yet to be tested on Windows.")
        fcg_go_path = os.path.join(directory, "FCG Go.exe")

    global fcg_go_process
    fcg_go_process = subprocess.Popen([fcg_go_path,
                                       '--port', str(port), 
                                       '--address', address])
    
    if fcg_go_process.poll():
        print("Connection to FCG Go failed (subprocess could not be started successfully).")
        return False
    else:
        time.sleep(2)
        # Shut down FCG Go when Python session is exited
        atexit.register(shutdown_fcg_go)
        return True
    

def shutdown_fcg_go():
    """Shut down FCG Go"""
    global fcg_go_process
    fcg_go_process.terminate()
    fcg_go_process = None


def restart_fcg_go():
    shutdown_fcg_go()
    init()