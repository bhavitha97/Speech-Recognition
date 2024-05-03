from flask import Flask, render_template, request
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import language_v1
import os
from pydub import AudioSegment

app = Flask(__name__)

# Load the path to the credentials file from environment variable
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# Check if the environment variable is set
if not GOOGLE_APPLICATION_CREDENTIALS:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

# Initialize Speech-to-Text client
speech_client = speech.SpeechClient.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

# Initialize Natural Language client
language_client = language_v1.LanguageServiceClient.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

UPLOADS_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

# Function to generate audio chunks
def generate_audio_chunks(audio_path):
    with open(audio_path, 'rb') as audio_file:
        while True:
            chunk = audio_file.read(4096)
            if not chunk:
                break
            yield chunk

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'file' not in request.files:
            return 'No file uploaded'

        audio_file = request.files['file']  # Access the uploaded file object
        if audio_file.filename == '':
            return 'No selected file'

        audio_path = os.path.join(UPLOADS_DIR, audio_file.filename)
        audio_file.save(audio_path)
        print(f"Audio file saved at: {audio_path}")
        print("Analyzing audio... This may take some time...")

        # Read the audio file and resample it to 16000 Hz
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(16000)

        # Split the resampled audio into chunks of 10 seconds each
        chunk_size_ms = 10000
        chunks = []
        for i in range(0, len(audio), chunk_size_ms):
            chunk = audio[i:i + chunk_size_ms]
            chunks.append(chunk)

        transcription = ""
        for i, chunk in enumerate(chunks):
            # Convert the chunk to raw PCM
            pcm_audio = chunk.raw_data

            # Configure Speech-to-Text client
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,  # Match the resampled sample rate
                language_code="en-US",
                enable_automatic_punctuation=True,
                enable_word_time_offsets=True
            )

            # Provide the chunk of audio content directly to the API
            audio_content = {"content": pcm_audio}
            print(f"Sending request for chunk {i+1}...")
            response = speech_client.recognize(config=config, audio=audio_content)
            print(f"Received response for chunk {i+1}")

            for result in response.results:
                transcription += result.alternatives[0].transcript + ' '

        print(f"Transcription: {transcription}")

        # Perform sentiment analysis with Natural Language API
        document = language_v1.Document(content=transcription, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = language_client.analyze_sentiment(request={'document': document}).document_sentiment

        sentiment_analysis = " "  # Initialize sentiment_analysis
        if sentiment.score > 0:
            sentiment_analysis = "Positive"
        elif sentiment.score < 0:
            sentiment_analysis = "Negative"
        else:
            sentiment_analysis = "Neutral"

        print(f"Sentiment Analysis: {sentiment_analysis}")
        print("Analysis completed successfully")

        return render_template('result.html', transcription=transcription, analysis=sentiment_analysis)

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return f'An error occurred during analysis. Please check the logs: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
