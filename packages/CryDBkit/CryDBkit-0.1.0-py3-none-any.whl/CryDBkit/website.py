import os
import sys
import zipfile
import wget
import pkg_resources


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


def show(db_file='CryDB.db'):
    """
    Set up the JSmol static resource and launch the ASE database viewer.

    This function performs the following steps:
    1. Checks if the `jsmol` folder is present in the ASE static directory.
    2. If not present, it downloads the required zip file from a remote server,
       extracts it, and prepares the folder structure.
    3. Creates a shell script `db.sh` that launches the ASE web viewer.
    4. Runs the shell script to display the database content.

    Parameters:
    - db_file (str): Name of the ASE database file to display (default: 'CryDB.db').
    """

    # URL to download the Jmol binary zip file (should contain jsmol.zip)
    file_url = 'https://figshare.com/ndownloader/files/46175526'

    # Determine the ASE package installation path
    ase_location = pkg_resources.get_distribution('ase').location
    static_folder = os.path.join(ase_location, 'ase', 'db', 'static')

    jsmol_path = os.path.join(static_folder, 'jsmol')

    # Check if JSmol is already installed in the static folder
    if not os.path.isdir(jsmol_path):
        print("JSmol not found; downloading required files...")

        # Download the archive to the static folder
        archive_path = wget.download(file_url, out=static_folder, bar=bar_progress)

        # Extract the main zip archive (assumes it’s named Jmol_binary.zip)
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(static_folder)

        # Locate and extract the jsmol.zip inside the extracted directory
        inner_jsmol_zip = os.path.join(static_folder, 'jmol-16.2.15', 'jsmol.zip')
        if os.path.exists(inner_jsmol_zip):
            with zipfile.ZipFile(inner_jsmol_zip, 'r') as zip_ref:
                zip_ref.extractall(static_folder)
        else:
            print("Error: jsmol.zip not found inside the downloaded archive.")
            return

        # Create a symlink (optional, not done here – can be added if necessary)

    print("Launching ASE database viewer (Linux/macOS only)...")

    # Bash script to open the ASE web viewer
    script_content = f"""#!/bin/bash
# Launch ASE Database Viewer
# Author: Cao Bin, HKUST.GZ

echo "Crystal Database Viewer - Cao Bin, HKUST.GZ"
ase db {db_file} -w
open http://10.5.151.180:5000
"""

    # Save and make the script executable
    with open('db.sh', 'w') as script_file:
        script_file.write(script_content)
    os.chmod('db.sh', 0o755)

    # Execute the script
    os.system('./db.sh')
