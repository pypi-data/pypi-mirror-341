import os
import sys
import zipfile
import wget
import pkg_resources
import platform
import webbrowser
import subprocess
import time
import requests


def bar_progress(current, total, width=80):
    """
    Display a progress bar during file download.

    Parameters:
    - current (int): Current number of bytes downloaded.
    - total (int): Total number of bytes to be downloaded.
    - width (int): Width of the progress bar (unused here).
    """
    progress_percentage = int(current / total * 100)
    progress_message = f"Downloading: {progress_percentage}% [{current} / {total}] bytes"
    sys.stdout.write(f"\r{progress_message}")
    sys.stdout.flush()


def detect_os():
    """
    Detect and print the current operating system.
    """
    os_name = platform.system()
    print(f"Current Operating System: {os_name}")
    return os_name


def wait_for_server(url, timeout=1000):
    """
    Wait for the server to be ready by sending HTTP requests until the server responds.

    Parameters:
    - url (str): The URL to check.
    - timeout (int): The maximum time (in seconds) to wait for the server.
    """
    print("Waiting for the server to start...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("\nServer started successfully!")
                return True
        except requests.ConnectionError:
            pass
        time.sleep(2)  # Wait for 1 second before retrying
        sys.stdout.write("^-^|")
        sys.stdout.flush()

    print("\nError: Server did not start within the timeout period.")
    return False


def show(db_file):
    """
    Set up the JSmol static resource and launch the ASE database viewer.

    Supports Windows, macOS, and Linux.

    Parameters:
    - db_file (str): Name of the ASE database file to display (default: 'CryDB.db').
    """

    # Detect and display OS
    current_os = detect_os()

    # JSmol download source (should contain jmol-*/jsmol.zip)
    file_url = 'https://figshare.com/ndownloader/files/46175526'
    ase_location = pkg_resources.get_distribution('ase').location
    static_folder = os.path.join(ase_location, 'ase', 'db', 'static')
    jsmol_path = os.path.join(static_folder, 'jsmol')

    # Download and extract JSmol if not already present
    if not os.path.isdir(jsmol_path):
        print("JSmol not found; downloading required files...")

        archive_path = wget.download(file_url, out=static_folder, bar=bar_progress)

        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(static_folder)

        inner_jsmol_zip = os.path.join(static_folder, 'jmol-16.2.15', 'jsmol.zip')
        if os.path.exists(inner_jsmol_zip):
            with zipfile.ZipFile(inner_jsmol_zip, 'r') as zip_ref:
                zip_ref.extractall(static_folder)
        else:
            print("Error: jsmol.zip not found inside the archive.")
            return

    print("Launching ASE database viewer...")

    # Launch ASE database viewer (assumes 'ase' command is available in PATH)
    try:
        subprocess.Popen(['ase', 'db', db_file, '-w'], shell=(current_os == 'Windows'))
    except FileNotFoundError:
        print("Error: ASE not found in system PATH.")
        return

    # Wait for the server to start
    if not wait_for_server("http://127.0.0.1:5000"):
        return

    # Open the web interface
    viewer_url = "http://127.0.0.1:5000"
    try:
        webbrowser.open(viewer_url)
    except Exception as e:
        print(f"Could not open browser: {e}")

    print(f"Viewer launched at {viewer_url}")


if __name__ == "__main__":
    show()
