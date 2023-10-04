from django_back.celery import app
from app_back_hospital.models import Consult, Patient
import speech_recognition as sr


@app.task
def process_audio(file_path, patient_id, unique_filename):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="pt-BR")
            except sr.UnknownValueError:
                print("No speech detected in the audio.")
                text = "Voz não reconhecida, ou audio esta sem voz"
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                text = "Error"

        patient = Patient.objects.get(id=patient_id)
        Consult.objects.create(
            patient=patient,
            converted_text=text,
            audio_path=file_path
        )

    except Exception as e:
        print(f"Erro ao processar áudio: {e}")
