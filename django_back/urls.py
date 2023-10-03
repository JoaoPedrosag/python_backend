
from django.contrib import admin
from django.urls import path

from app_back_hospital import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.upload_audio, name='upload_audio'),
    path('all_pacientes/', views.get_all_pacientes, name='all_pacientes'),
    path('consultas/<int:patient_id>', views.get_consultas_by_paciente, name='consultas_by_paciente'),
    path('download/<int:consult_id>', views.download_audio, name='download_audio'),
]
