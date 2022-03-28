from os import name
from django.urls import  path
from . import  views 
app_name = 'CandidatosMaestria'
urlpatterns =  [
    #path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/',views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/',views.ResultsView.as_view(),name='results'),
    path('<int:estatus_id>/asignar/',views.asignar,name='asignar'),
    path('Login/',views.Login,name='Login'),
    path('Registro/',views.Registro,name='Registro'),
    path('',views.index,name='index'),
    path('UploadFile/',views.UploadFile,name='UploadFile'),
    path('Riquisito/<int:requisito_id>/',views.Subir,name='Subir'),
    path('Logout/',views.Logout,name='Logout'),
    path('Maestro/',views.Maestro,name='Maestro'),
    path('ListarCursos/',views.ListarCursos,name='ListarCursos'),
    path('Curso/<int:idCurso>/',views.Curso,name='Curso'), 
    path('Entrevista/',views.entrevista,name='Entrevista'),
    path('CursosDocente/',views.CursosDocente,name='CursosDocente'),
    path('CursoSave/',views.CursoSave,name='CursoSave'),
    path('EntrevistasDocente/',views.EntrevistasDocente,name='EntrevistasDocente'),
    path('Encuesta/<int:identrevista>/',views.Encuestas,name='Encuesta'),
    path('VerEncuesta/<int:identrevista>/',views.VerEncuesta,name='VerEncuesta'),
    path('PdfEncuesta/<int:identrevista>/',views.PdfEncuesta,name='PdfEncuesta'),
    path('SaveEncuesta/',views.SaveEncuesta,name='SaveEncuesta'),
    path('Ponencia/<int:identrevista>/',views.ponencia,name='Ponencia'),
    path('SavePonencia/',views.SavePonencia,name='SavePonencia'),
    path('Verponencia/<int:identrevista>/',views.Verponencia,name='Verponencia'), 
    path('PdfPonencia/<int:identrevista>/',views.PdfPonencia,name='PdfPonencia'), 
    
    
    
]

