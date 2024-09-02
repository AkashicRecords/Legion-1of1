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

def setup_sub_agents():
    venv_name = "myenv"
    python_path = os.path.join(venv_name, 'bin', 'python')
    pip_path = os.path.join(venv_name, 'bin', 'pip')

    packages = [
        # Add packages for sub-agents here
        "nltk",
        "spacy",
        "transformers",
        "torch",
        "scikit-learn",
        "face_recognition",
        "biosppy",
        "Pillow",
        "matplotlib"
    ]

    print("Installing sub-agent-specific packages...")
    logging.info("Installing sub-agent-specific packages...")
    for package in packages:
        print(f"Installing {package}...")
        success = run_command(f'"{pip_path}" install "{package}"')
        if not success:
            print(f"Failed to install {package}. Check the log for details.")
            logging.error(f"Failed to install {package}")

    print("Sub-agent environment setup complete.")
    logging.info("Sub-agent environment setup complete.")

if __name__ == "__main__":
    log_filename = 'sub_agents_setup.log'
    logging.basicConfig(filename=log_filename, 
                        level=logging.INFO, 
                        format='%(asctime)s - %(levellevel)s - %(message)s',
                        filemode='w')

    logging.info(f"Starting sub-agent environment setup at {datetime.now()}")
    setup_sub_agents()
    logging.info(f"Finished sub-agent environment setup at {datetime.now()}")

    print(f"Sub-agent setup complete. Check {log_filename} for details.")