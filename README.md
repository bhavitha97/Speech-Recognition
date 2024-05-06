# Speech Recognition Web App

This Flask web application performs speech-to-text transcription and sentiment analysis on uploaded audio files using Google Cloud Speech-to-Text and Natural Language APIs.

## Installation

1. **Clone the Repository**: Clone this repository to your local machine using Git:

    ```bash
    git clone <repository_url>
    ```

2.**Create the Project Directory**: Create a project folder in your working directory:

    mkdir speech-analysis-flask-app


3. **Navigate to the Project Directory**: Change your working directory to the project folder:

    ```bash
    cd speech-analysis-flask-app
    ```

4. **Install Dependencies**: Install the required Python dependencies listed in `requirements.txt`. It's recommended to use a virtual environment to manage dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up Google Cloud Credentials**: Make sure you have a Google Cloud Platform (GCP) account and create a service account with the necessary permissions for using Speech-to-Text and Natural Language APIs. Download the service account key file (JSON) and set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of this file.

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account_key.json
    ```

    Replace `/path/to/service_account_key.json` with the actual path to your service account key file.

## Running the Application in VSCode

To run the Flask application in VSCode, follow these steps:

1. **Open VSCode**: Open Visual Studio Code.

2. **Open Project**: Open the cloned project folder using VSCode.

3. **Set up Debug Configuration**: In VSCode, go to the debug view (or press `Ctrl + Shift + D`). Click on the gear icon to create a new `launch.json` file for debugging.

4. **Add Configuration**: Click on "Add Configuration" and select "Flask" from the dropdown menu. This will generate a basic launch configuration for Flask applications.

5. **Configure Launch Settings**: Modify the generated `launch.json` file to specify the path to the Flask app file (`app.py`), the environment variables, and any other necessary settings.

6. **Start Debugging**: Press `F5` or click on the "Start Debugging" button to start the Flask application in debug mode.

7. **Access the Application**: Once the Flask app is running, open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage

1. **Upload Audio File**: On the homepage of the application, click on the "Choose File" button to select an audio file for analysis.

2. **Analyze Audio**: After selecting the file, click on the "Analyze" button to initiate the analysis process. The application will transcribe the audio to text and perform sentiment analysis on the transcribed text.

3. **View Results**: Once the analysis is complete, the results will be displayed on a new page, showing the transcription of the audio and the sentiment analysis.

## Troubleshooting

- **Environment Variables**: Ensure that the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is properly set to the path of your GCP service account key file.

- **File Upload Limit**: If you encounter issues with file uploads, check the maximum file size limit configured in the Flask application (`MAX_CONTENT_LENGTH`).

- **Debugging**: If you encounter errors or issues while running the application in VSCode, check the debug console for error messages and consult the Flask documentation for troubleshooting.

## License

This project is licensed under the [MIT License](LICENSE).
