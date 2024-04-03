from django.shortcuts import render
from django.http import JsonResponse
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Deepgram API key
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

# OpenAI Client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )


# Deepgram options
OPTIONS = PrerecordedOptions(
    model="nova-2",
    language="en",
    smart_format=True,
    diarize=True,
)

def transcribe_uploaded_audio(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        try:
            # Transcribe the audio using Deepgram
            deepgram = DeepgramClient(DEEPGRAM_API_KEY)
            payload: FileSource = {
                "buffer": audio_file.read(),
            }
            response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, OPTIONS)
            response_json = json.loads(response.to_json())

            # Extract conversation turns
            conversation_turns = extract_conversation_turns(response_json)
            conversation = "\n\n".join(conversation_turns)
            print(conversation)
            # Perform sentiment analysis using OpenAI's Chat Completions API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                            {"role": "system", "content": "Step into the role of a behavioral psychologist studying the conversation from a scientific perspective." +
                                                          "Analyze the speakers' language patterns and tone to uncover insights into their personality traits, motivations, and potential biases." +
                                                         "Discuss how these factors may be shaping their interaction and offer recommendations for enhancing their self-awareness and interpersonal skills."},
                            {"role": "user", "content": f"Analyze the sentiment and provide psychological insights for each speaker in the following conversation:\n\n{conversation}\n\n" +
                                "go speaker by speaker and replace the dialogue with your sentiment analysis. Don't output anything else other than the analysis for each speaker, insights, and recommendations" +
                                 "as an emotional coach. Insights:"}
                        ]
                )
            
            insights = response.choices[0].message.content
            print(insights)
            return JsonResponse({'conversation': conversation, 'insights': insights})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'No audio file provided'}, status=400)

def extract_conversation_turns(response_json):
    conversation_turns = []
    current_speaker = None
    current_turn = ""

    for word in response_json['results']['channels'][0]['alternatives'][0]['words']:
        speaker_id = word['speaker']
        if speaker_id != current_speaker:
            if current_turn:
                conversation_turns.append(f"[Speaker:{current_speaker}] {current_turn.strip()}")
            current_speaker = speaker_id
            current_turn = ""
        current_turn += f"{word['word']} "

    if current_turn:
        conversation_turns.append(f"[Speaker:{current_speaker}] {current_turn.strip()}")

    return conversation_turns

def upload_audio_view(request):
    return render(request, 'conversation/upload_audio.html')