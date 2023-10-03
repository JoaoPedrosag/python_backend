import os
import shutil
import subprocess
import uuid
from time import timezone

from django.http import JsonResponse, HttpResponseBadRequest, Http404, HttpResponse
import speech_recognition as sr
import tempfile

from django.views.decorators.csrf import csrf_exempt
from pydub import AudioSegment

from .models import Patient, Consult

transcriptions = {}

recognizer = sr.Recognizer()


@csrf_exempt
def upload_audio(request):
    try:
        if request.method == 'POST':
            file = request.FILES['file']
            name = request.POST.get('name')
            patient_id = request.POST.get('id')
            print(file)

            patient, created = Patient.objects.get_or_create(id=patient_id, defaults={'name': name})
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.aac') as temp_file:
                    for chunk in file.chunks():
                        temp_file.write(chunk)

            except Exception as e:
                print(f'Erro ao criar arquivo temporário: {e}')
                return JsonResponse({'status': 'error', 'message': 'Erro ao criar arquivo temporário'})
            wav_temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            wav_temp_file.close()
            convert_audio(temp_file.name, wav_temp_file.name)
            audio_dir = './audios'
            if not os.path.exists(audio_dir):
                os.makedirs(audio_dir)

            unique_filename = str(uuid.uuid4())
            saved_audio_path = os.path.join(audio_dir, f"{unique_filename}.wav")
            shutil.move(wav_temp_file.name, saved_audio_path)

            with sr.AudioFile(saved_audio_path) as source:

                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language="pt-BR")
                except sr.UnknownValueError:
                    print("No speech detected in the audio.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
            consult = Consult.objects.create(
                patient=patient,
                converted_text=text,
                audio_path=saved_audio_path
            )

            return JsonResponse({'status': 'success', 'converted_text': consult.converted_text})
        else:
            return HttpResponseBadRequest('Method not allowed')
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def convert_audio(input_path, output_path):
    try:
        sound = AudioSegment.from_file(input_path, format="aac")
        sound = sound.set_channels(1).set_frame_rate(16000)
        sound.export(output_path, format="wav")
    except Exception as e:
        print(f"Erro ao converter o áudio com PyDub: {e}")


def get_consultas_by_paciente(request, patient_id):
    consults = Consult.objects.filter(patient_id=patient_id).values('id', 'converted_text', 'consultation_date',
                                                                    'audio_path')
    consults_list = list(consults)
    return JsonResponse(consults_list, safe=False)


def get_all_pacientes(request):
    patients = Patient.objects.all().values('id', 'name')
    patients_list = list(patients)
    print(patients_list)
    return JsonResponse(patients_list, safe=False)


def download_audio(request, consult_id):
    try:
        consult = Consult.objects.get(id=consult_id)
    except Consult.DoesNotExist:
        raise Http404("Consulta não encontrada")

    audio_path = consult.audio_path

    if os.path.exists(audio_path):
        with open(audio_path, 'rb') as f:
            response = HttpResponse(f, content_type='audio/wav')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(audio_path)}"'
            return response
    else:
        return HttpResponse('Arquivo não encontrado', status=404)
