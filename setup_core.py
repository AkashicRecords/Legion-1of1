import os
import sys
import subprocess
import platform
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

def setup_core():
    venv_name = "myenv"
    
    os_name = platform.system().lower()
    print(f"Detected OS: {os_name}")
    logging.info(f"Detected OS: {os_name}")

    print("Creating virtual environment...")
    logging.info("Creating virtual environment...")
    run_command(f"{sys.executable} -m venv {venv_name}")

    if os_name in ['linux', 'darwin']:
        python_path = os.path.join(venv_name, 'bin', 'python')
        pip_path = os.path.join(venv_name, 'bin', 'pip')
    elif os_name == 'windows':
        python_path = os.path.join(venv_name, 'Scripts', 'python.exe')
        pip_path = os.path.join(venv_name, 'Scripts', 'pip.exe')
    else:
        logging.error(f"Unsupported OS: {os_name}")
        sys.exit(1)

    print("Updating pip, setuptools, and wheel...")
    logging.info("Updating pip, setuptools, and wheel...")
    run_command(f'"{python_path}" -m pip install --upgrade pip setuptools wheel')

    packages = [
        "numpy",
        "pandas",
        "urllib3<2.0",
        "requests",
        "pyyaml",
        "redis",
        "sqlalchemy",
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-multipart",
        "aiohttp",
        "importlib-metadata<5.0",
        "vine<5.0",
        "kombu<5.0",
        "billiard<4.0",
        "celery==4.4.7"
    ]

    print("Installing packages...")
    logging.info("Installing packages...")
    for package in packages:
        print(f"Installing {package}...")
        success = run_command(f'"{pip_path}" install "{package}"')
        if not success:
            print(f"Failed to install {package}. Check the log for details.")
            logging.error(f"Failed to install {package}")

    print("Upgrading Celery without dependencies...")
    logging.info("Upgrading Celery without dependencies...")
    success = run_command(f'"{pip_path}" install --upgrade --no-deps celery==4.4.7')
    if not success:
        print("Failed to upgrade Celery. Check the log for details.")
        logging.error("Failed to upgrade Celery")

    print("Virtual environment setup complete.")
    logging.info("Virtual environment setup complete.")

if __name__ == "__main__":
    log_filename = 'venv_setup.log'
    logging.basicConfig(filename=log_filename, 
                        level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='w')

    logging.info(f"Starting virtual environment setup at {datetime.now()}")
    setup_core()
    logging.info(f"Finished virtual environment setup at {datetime.now()}")

    print(f"Setup complete. Check {log_filename} for details.")
    print("To activate the virtual environment:")
    if platform.system().lower() in ['linux', 'darwin']:
        print("source myenv/bin/activate")
    elif platform.system().lower() == 'windows':
        print("myenv\\Scripts\\activate.bat")