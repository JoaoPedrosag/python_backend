from time import timezone

from django.http import JsonResponse, HttpResponseBadRequest
import speech_recognition as sr
import tempfile

from django.views.decorators.csrf import csrf_exempt

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

            patient, created = Patient.objects.get_or_create(id=patient_id, defaults={'name': name})

            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)

            with sr.AudioFile(temp_file.name) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="pt-BR")

            consult = Consult.objects.create(patient=patient, converted_text=text)

            return JsonResponse({'status': 'success', 'converted_text': consult.converted_text})
        else:
            return HttpResponseBadRequest('Method not allowed')
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def get_consultas_by_paciente(request, patient_id):
    consultas = Consulta.objects.filter(paciente_id=patient_id).values('texto_convertido', 'data_consulta')
    consultas_list = list(consultas)
    return JsonResponse(consultas_list, safe=False)

def get_all_pacientes(request):
    pacientes = Paciente.objects.all().values('id', 'name')
    pacientes_list = list(pacientes)
    print(pacientes_list)
    return JsonResponse(pacientes_list, safe=False)
