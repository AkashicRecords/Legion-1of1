import subprocess
import sys
import logging
from datetime import datetime

def install_libraries():
    libraries = [
        "nltk",        # Natural Language Processing
        "spacy",       # Natural Language Processing
        "transformers",# NLP models from Hugging Face (for using models like LLAMA)
        "torch",       # PyTorch for deep learning
        "scikit-learn",# Machine learning library
        "pandas",      # Data manipulation and analysis
        "numpy",       # Numerical computing
        "requests"     # HTTP library for making requests
    ]

    # Get the path to the pip associated with the current Python interpreter
    pip_path = [sys.executable, "-m", "pip"]

    for lib in libraries:
        try:
            logging.info(f"Installing {lib}...")
            subprocess.check_call(pip_path + ["install", "--upgrade", "pip"])
            subprocess.check_call(pip_path + ["install", "--user", lib], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT)
            logging.info(f"Successfully installed {lib}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install {lib}. Error: {e.output.decode()}")

if __name__ == "__main__":
    # Set up logging
    log_filename = 'library_installation.log'
    logging.basicConfig(filename=log_filename, 
                        level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='w')  # 'w' mode overwrites the file each time

    logging.info(f"Starting library installation at {datetime.now()}")
    
    install_libraries()
    
    logging.info(f"Finished library installation at {datetime.now()}")

    print(f"Installation complete. Check {log_filename} for details.")