from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.core import exceptions
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError


from .models import Alumno,DetalleRequisito, Periodo, Semestre,EstatusRequisitoAlumno,Requisito

def index(request):
    if request.user.is_authenticated:

        try:
            alumno01 = Alumno.objects.get(Usuario=request.user)
        except Alumno.DoesNotExist:
            return HttpResponseRedirect(reverse('AlumnosMaestria:Logout'))
        
        requisitossemestre = Requisito.objects.order_by('pk').filter(semestre=alumno01.alumnosemestre)
        listasemestre= Semestre.objects.order_by('pk') 
        ListaRequisitos = []

        
        for requisitos in requisitossemestre:
            ListaRequisitos.append(get_object_or_404(DetalleRequisito,alumno=alumno01, requisito=requisitos) )
        return render(request,'AlumnosMaestria/index.html',{'alumno':alumno01,'ListaRequisitos':ListaRequisitos,'listasemestre':listasemestre})
        
    return HttpResponseRedirect(reverse('AlumnosMaestria:Login'))


def Login(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('AlumnosMaestria:index'))
        
    if request.method=='POST':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('AlumnosMaestria:index'))
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    alumno = Alumno.objects.get(Usuario=user)
                except Alumno.DoesNotExist:
                    logout(request)
                    return render(request,'AlumnosMaestria/Login.html',{'error_message':'La Cuenta No Tiene Accesso'})
                return HttpResponseRedirect(reverse('AlumnosMaestria:index'))
            else:
                return render(request,'AlumnosMaestria/Login.html',{'error_message':'Cuenta o Contraseña Equivocada'})
    else:
        return render(request, 'AlumnosMaestria/Login.html')
    
def Registro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('AlumnosMaestria:index'))
    else:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            email= request.POST['email']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return render(request, 'AlumnosMaestria/Registro.html',{'error_message':'El usuario ya Existe'})
            
            user = User.objects.create_user(username,email,password)
            semestre = get_object_or_404(Semestre, pk=1)
            periodoA= Periodo.objects.order_by('pk').last()
            try: 
                alumno = Alumno.objects.create(nombre=request.POST['nombre'],apellidopaterno=request.POST['apellidopaterno'],apellidomaterno=request.POST['apellidomaterno'],curp=request.POST['curp'],email=user.email,NumeroControl=request.POST['numerocontrol'], alumnosemestre=semestre,Usuario=user,periodo=periodoA)
            except 	IntegrityError:
                user.delete()
                return render(request, 'AlumnosMaestria/Registro.html',{'error_message':'El verifique sus informacion'})
            
            
            
            return HttpResponseRedirect(reverse('AlumnosMaestria:Login'))
        else:
            return render(request, 'AlumnosMaestria/Registro.html')
        
  


def UploadFile(request):


    if request.method == "POST":
        
        # Fetching the form data
        

        # Saving the information in the database
        if request.FILES:
            fecha=datetime.now()
            requitisoid = request.POST['id']
            ListaRequisitos=get_object_or_404(DetalleRequisito,id=requitisoid)
            status =get_object_or_404(EstatusRequisitoAlumno,pk=2)
            ListaRequisitos.ruta = request.FILES['uploadedFile']
            ListaRequisitos.estatusrequisitoalumno=status
            ListaRequisitos.carga=fecha
            ListaRequisitos.observaciones=" "
            ListaRequisitos.save()
        else:
            return HttpResponseRedirect(reverse('AlumnosMaestria:index'))

    return HttpResponseRedirect(reverse('AlumnosMaestria:index'))

def Subir(request,requisito_id):
    requisitoAlumno= get_object_or_404(DetalleRequisito,pk=requisito_id)

    return render(request, 'AlumnosMaestria/Archivos.html',{'requisito_id':requisitoAlumno.id,'Descripcion':requisitoAlumno.requisito.descripcion,'size':(requisitoAlumno.requisito.tamallo * 1000000)})

def VSemestre(request,semestre_id):
    if request.user.is_authenticated:

        try:
            alumno01 = Alumno.objects.get(Usuario=request.user)
        except Alumno.DoesNotExist:
            return HttpResponseRedirect(reverse('AlumnosMaestria:Logout'))
        requisitossemestre = Requisito.objects.filter(semestre=semestre_id)
        listasemestre= Semestre.objects.all() 
        ListaRequisitos = []
        
        for requisitos in requisitossemestre:
            ListaRequisitos.append(get_object_or_404(DetalleRequisito,alumno=alumno01, requisito=requisitos) )
        return render(request,'AlumnosMaestria/index.html',{'alumno':alumno01,'ListaRequisitos':ListaRequisitos,'listasemestre':listasemestre})
        
    return HttpResponseRedirect(reverse('AlumnosMaestria:Login'))



def Logout(request):
    if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect(reverse('AlumnosMaestria:Login'))
    return HttpResponseRedirect(reverse('AlumnosMaestria:Login'))