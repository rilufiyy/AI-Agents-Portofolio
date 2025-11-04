
import os
import sounddevice as sd
import scipy.io.wavfile as wavfile
from playsound import playsound
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def record_voice(filename="user.wav", duration=5, sample_rate=44100):
    print("Silakan bicara (5 detik)...")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    wavfile.write(filename, sample_rate, audio)
    print("Rekaman selesai.\n")
    return filename

def speech_to_text(audio_path):
    with open(audio_path, "rb") as f:
        text = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="text"
        )
    print("Kamu bilang:", text, "\n")
    return str(text)


def ask_ai(user_text, chat_history):
    chat_history.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_history,
        temperature=0.7,
    )

    ai_answer = response.choices[0].message.content
    print("AI:", ai_answer, "\n")

    chat_history.append({"role": "assistant", "content": ai_answer})
    return ai_answer, chat_history


def text_to_speech(text, out_file="assistant.mp3"):
    out_path = Path(out_file)
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    ) as resp:
        resp.stream_to_file(out_path)
    print("Memutar suara AI...\n")
    playsound(str(out_path))


def main():
    print("Voice Chat AI")
    print("Ketik 'exit' kapan saja untuk keluar.\n")

    chat_history = [
        {"role": "system", "content": "Kamu adalah asisten AI yang ramah, jawab singkat dan santai dalam bahasa Indonesia."}
    ]  

    while True:
        audio_path = record_voice(duration=5)
        user_text = speech_to_text(audio_path).strip().lower()

        if "exit" in user_text or "keluar" in user_text:
            print("Sampai jumpa!")
            break

        ai_text, chat_history = ask_ai(user_text, chat_history)
        text_to_speech(ai_text)

if __name__ == "__main__":
    main()