# Orchestration Agent

## Overview
Orchestration Agent is a Python-based project that sets up a virtual environment for an orchestration system capable of delegating tasks to various sub-agents for data processing, including audio, video, voice-to-text, facial recognition, and biometric data analysis.

## Requirements
- Python 3.7 or higher
- pip (will be updated during setup)
- Google Cloud Firestore (for long-term memory storage)

## Installation

1. Clone the repository:
   ```
   git clone [your-repository-url]
   cd [repository-name]
   ```

2. Run the core setup script:
   ```
   python Orcastration_Agent/setup_core.py
   ```

   This script will:
   - Create a virtual environment named 'myenv'
   - Install required core packages for orchestration

3. (Optional) Run the mobile setup script:
   ```
   python Orcastration_Agent/setup_mobile.py
   ```

   This script will:
   - Install mobile-specific packages

4. (Optional) Run the cloud setup script:
   ```
   python Orcastration_Agent/setup_cloud.py
   ```

   This script will:
   - Install cloud-specific packages

5. (Optional) Run the sub-agent setup script:
   ```
   python Orcastration_Agent/setup_sub_agents.py
   ```

   This script will:
   - Install sub-agent-specific packages

6. Activate the virtual environment:
   - On Linux/macOS:
     ```
     source myenv/bin/activate
     ```
   - On Windows:
     ```
     myenv\Scripts\activate.bat
     ```

7. Verify the installation:
   ```
   python Orcastration_Agent/verify_libraries.py
   ```
## Setting up a Virtual Environment

To isolate the project dependencies and ensure a clean development environment, it's recommended to use a virtual environment. Follow these steps:

1. Navigate to the project directory:
   ```
   cd path/to/Orcastration_Agent
   ```

2. Create a new virtual environment:
   ```
   python3 -m venv myenv
   ```

3. Activate the virtual environment:
   - On macOS and Linux:
     ```
     source myenv/bin/activate
     ```
   - On Windows:
     ```
     myenv\Scripts\activate
     ```

4. Your prompt should change to indicate that the virtual environment is active.

5. Run the setup scripts within this environment:
   ```
   python setup_core.py
   python setup_mobile.py
   python setup_cloud.py
   python setup_sub_agents.py
   ```

6. Verify the installation:
   ```
   python verify_libraries.py
   ```

7. You can now run the main orchestration agent script:
   ```
   python orchestration_agent.py
   ```

Remember to activate the virtual environment each time you work on the project. When you're done, you can deactivate the environment by typing:
## Configuration

1. Create a `config.json` file to specify sub-agents and task routing:
   ```json
   {
       "sub_agents": {
           "data_ingestion_agent": {
               "module": "Orcastration_Agent.sub_agents.data_ingestion_agent",
               "class": "DataIngestionAgent"
           },
           "data_validation_agent": {
               "module": "Orcastration_Agent.sub_agents.data_validation_agent",
               "class": "DataValidationAgent"
           },
           "computer_vision_agent": {
               "module": "Orcastration_Agent.sub_agents.computer_vision_agent",
               "class": "ComputerVisionAgent"
           },
           "nlp_agent": {
               "module": "Orcastration_Agent.sub_agents.nlp_agent",
               "class": "NLPAagent"
           },
           "output_finalization_agent": {
               "module": "Orcastration_Agent.sub_agents.output_finalization_agent",
               "class": "OutputFinalizationAgent"
           },
           "reinforcement_learning_agent": {
               "module": "Orcastration_Agent.sub_agents.reinforcement_learning_agent",
               "class": "ReinforcementLearningAgent"
           }
       },
       "task_routing": {
           "image": ["computer_vision_agent"],
           "text": ["data_ingestion_agent", "data_validation_agent", "nlp_agent", "output_finalization_agent"],
           "audio": ["data_ingestion_agent", "data_validation_agent"]
       },
       "cloud_storage": {
           "project_id": "your-google-cloud-project-id",
           "collection_name": "long_term_memory"
       }
   }
   ```

2. Modify the `config.json` file to add more sub-agents and task routing as needed.

## Usage

After installation and activation of the virtual environment, you can start the orchestration agent:
   ```
   python Orcastration_Agent/orchestration_agent.py
   ```

## Included Libraries

- Data handling: numpy, pandas
- Networking: requests, aiohttp
- Task queue and message broker: Celery, Redis
- Database ORM: SQLAlchemy
- API framework: FastAPI, Uvicorn
- Data validation: Pydantic
- Configuration management: PyYAML
- Cloud storage: google-auth-oauthlib, google-auth-httplib2, google-api-python-client

## Troubleshooting

- Check the `venv_setup.log` file for detailed information about the setup process.
- Check the `library_verification.log` file for detailed information about the library verification process.
- If you encounter issues with specific libraries, ensure your Python version is compatible.

## Contributing

[Include guidelines for contributing to the project]

## License

[Specify the license under which this project is released]

## Storage

This application supports both local storage on SD card (when available) and cloud storage using Google Drive.

### SD Card Storage
If an SD card is available and properly mounted, the application will store its database and temporary files on the SD card. This provides additional storage space and potentially allows the application to run from the SD card.

### Cloud Storage
The application can sync its database to Google Drive for backup and accessibility across devices. To set up cloud storage:

1. Enable the Google Drive API in your Google Cloud Console.
2. Create credentials (OAuth client ID) for a desktop application.
3. Download the credentials and save them as `credentials.json` in the application directory.
4. Run the cloud setup script:
   ```
   python Orcastration_Agent/cloud_setup.py
   ```
   This will guide you through the OAuth flow and save the resulting token.

## Running from SD Card

To allow the application to be installed on the SD card, the Android app's `AndroidManifest.xml` file includes the `android:installLocation="preferExternal"` attribute. Note that not all devices support running apps from SD cards, and performance may vary.