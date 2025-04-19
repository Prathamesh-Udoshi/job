from gtts import gTTS
import os

def translate_and_speak(text, lang='hi'):
    tts = gTTS(text, lang=lang)
    audio_path = 'static/output.mp3'
    tts.save(audio_path)
    return audio_path
