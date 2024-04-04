# Conversation AI

Conversation AI is a web application that transcribes audio conversations and provides psychological insights and sentiment analysis for the speakers involved. The application utilizes the Deepgram API for speech-to-text transcription and OpenAI's GPT-3.5-turbo model for generating insightful analysis of the conversation.

## Features

- Upload audio files containing conversations between multiple speakers
- Transcribe the audio using Deepgram's speech-to-text API
- Extract conversation turns and assign them to individual speakers
- Perform sentiment analysis and provide psychological insights for each speaker using OpenAI's GPT-3.5-turbo model
- Display the transcribed conversation and generated insights in a user-friendly web interface

## Prerequisites

- Docker
- Deepgram API key
- OpenAI API key

## Setup and Installation

1. Clone the repository:
```
git clone https://github.com/gchoi5738/conversation-ai.git
cd conversation-ai/conversation_ai
```

2. Create a `.env` file in the project root directory and add your API keys. Should be in the same directory as the requirements.txt:
```
DEEPGRAM_API_KEY=your-deepgram-api-key
OPENAI_API_KEY=your-openai-api-key
```

Replace `your-deepgram-api-key` and `your-openai-api-key` with your actual API keys.

3. Build the Docker image:
```
docker build -t conversation-ai .
```


4. Run the Docker container:
```
docker run -p 8000:8000 --env-file .env conversation-ai
```

5. Access the application in your web browser at `http://localhost:8000`.

## Usage

1. Open the application in your web browser.
2. Click on the "Choose File" button and select an audio file containing a conversation (supported formats: MP3, WAV, OGG).
3. Click the "Transcribe" button to start the transcription and analysis process.
4. Wait for the application to transcribe the audio and generate insights (this may take a few moments).
5. Once the process is complete, the transcribed conversation and psychological insights will be displayed on the page.

Note: For longer audio files (> 5 minutes), the transcription process may take more time to complete.

## Troubleshooting

- If you encounter an error during transcription, try uploading the audio file again. Sometimes the server may take a few moments to set up and process the request.
- Ensure that your API keys are valid and have the necessary permissions.
- Check the browser console for any error messages or logs that may provide additional information.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgements

- [Deepgram](https://deepgram.com/) for providing the speech-to-text API
- [OpenAI](https://openai.com/) for providing the GPT-3.5-turbo model for sentiment analysis and psychological insights