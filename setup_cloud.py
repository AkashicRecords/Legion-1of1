import os
import subprocess
import logging
from datetime import datetime

def run_command(command, ignore_errors=False):
    try:
        print(f"Running command: {command}")
        result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
        print(f"Command output: {result.stdout}")
        logging.info(f"Command output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        print(f"Error output: {e.stderr}")
        logging.error(f"Command failed: {e}")
        logging.error(f"Error output: {e.stderr}")
        if not ignore_errors:
            sys.exit(1)
        return False

def setup_cloud():
    venv_name = "myenv"
    python_path = os.path.join(venv_name, 'bin', 'python')
    pip_path = os.path.join(venv_name, 'bin', 'pip')

    packages = [
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client"
    ]

    print("Installing cloud-specific packages...")
    logging.info("Installing cloud-specific packages...")
    for package in packages:
        print(f"Installing {package}...")
        success = run_command(f'"{pip_path}" install "{package}"')
        if not success:
            print(f"Failed to install {package}. Check the log for details.")
            logging.error(f"Failed to install {package}")

    print("Cloud environment setup complete.")
    logging.info("Cloud environment setup complete.")

if __name__ == "__main__":
    log_filename = 'cloud_setup.log'
    logging.basicConfig(filename=log_filename, 
                        level=logging.INFO, 
                        format='%(asctime)s - %(levellevel)s - %(message)s',
                        filemode='w')

    logging.info(f"Starting cloud environment setup at {datetime.now()}")
    setup_cloud()
    logging.info(f"Finished cloud environment setup at {datetime.now()}")

    print(f"Cloud setup complete. Check {log_filename} for details.")