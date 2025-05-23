import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import whisper
import os

# Sample rate (16K) higher samplerate = better sound quality
samplerate = 16000
# Duration of the recording
duration = 5
# mono recording
channels = 1
# loads the model for whisper AI
# You can choose from: (tiny, base, small, medium, large, turbo)
# Turbo is not higher quality but its really fast
model = whisper.load_model("turbo")

def record_audio():
    """Records audio from the microphone"""
    try:
        # Records the audio and saves it as 'audio'
        audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, dtype='int16')

        # Wait for the recording to finish
        sd.wait()

        # makes a temporary audio file (.wav) and saves the recorded audio into this file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            write(tmpfile.name, samplerate, audio)
            return tmpfile.name
    except Exception as e:
        return None

def transcribe_audio(file_path):
    """Transcribes audio file to text"""
    try:
        if not file_path:
            return "Cannot record audio, try again please..."
            
        # Transcribe the audio to text
        result = model.transcribe(file_path)
        
        # Remove temporary file after transcription
        try:
            os.remove(file_path)
        except:
            pass

        # Get the text out of the transcribe results
        return result['text']
    except Exception as e:
        # Try to clean up the file even if transcription failed
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
            
        return "There was a problem turning the audio into text, please submit a new voice message"

def get_speech_input():
    """Gets speech input from user"""
    # Record audio
    audio_path = record_audio()

    # Conforming message if the recording ended
    print("🎤 Recording finished!")
    
    # Transcribe the audio
    transcription = transcribe_audio(audio_path)
    
    # Return just the transcription
    return transcription