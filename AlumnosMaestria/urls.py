from django.urls import  path
from . import  views 
app_name = 'AlumnosMaestria'
urlpatterns =  [
    path('', views.index, name='index'),
    path('Login/',views.Login,name='Login'),
    path('Registro/',views.Registro,name='Registro'),
    path('UploadFile/',views.UploadFile,name='UploadFile'),
    path('Riquisito/<int:requisito_id>/',views.Subir,name='Subir'),
      path('Semestre/<int:semestre_id>/',views.VSemestre,name='Semestre'),
    path('Logout/',views.Logout,name='Logout'),
]