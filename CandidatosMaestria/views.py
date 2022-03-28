from typing import ChainMap
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import context, loader
from .models import Aspirante, CatalogoPregunta, Criterio, DetalleCriterioRubrica, DetalleEncuesta, DetalleEntrevista, DetallePonencia, Docente, Encuesta, Entrevista, EstatusAspirante, Periodo, Ponencia,Requisito,EstatusRequisitoEstudiante,DetalleRequisito,DetalleAspiranteCurso,CursoPropedeutico, StatusEntrevista
from django.urls import reverse
from django.views import generic
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .utils import render_to_pdf
from django.db import IntegrityError






"""def index(request):
    latest_estatusalumno_list = EstatusAlumno.objects.order_by('estatus')
    context = {'latest_estatusalumno_list':latest_estatusalumno_list,}
    return render(request,'CandidatosMaestria/Index.html',context)
    template= loader.get_template('CandidatosMaestria/Index.html')
    return HttpResponse(template.render(context,request))

    output = ','.join([q.descripcion for q in latest_estatusalumno_list])    
    return HttpResponse(output)"""


class IndexView(generic.ListView):
    template_name = 'CandidatosMaestria/index.html'
    context_object_name = 'latest_estatusalumno_list'
    
    def get_queryset(self):
        """Return the last five published questions."""
        return EstatusAspirante.objects.order_by('estatus')




"""def detail(request, estatus_id):
    
    try:
        estatusalumno = EstatusAlumno.objects.get(pk=estatus_id)
    except EstatusAlumno.DoesNotExist:
        raise Http404("Estatus no Existe")
    return render(request,'CandidatosMaestria/detail.html',{'estatusalumno':estatusalumno})
    

    estatusalumno = get_object_or_404(EstatusAlumno,pk=estatus_id)
    return render(request,'CandidatosMaestria/detail.html',{'estatusalumno':estatusalumno})"""

class DetailView(generic.DetailView):
    model = EstatusAspirante
    template_name = 'CandidatosMaestria/detail.html'
   

"""def results(request, estatus_id):
    estatusalumno = get_object_or_404(EstatusAlumno, pk=estatus_id)
    return render(request, 'CandidatosMaestria/results.html', {'estatusalumno': estatusalumno})"""


class ResultsView(generic.DetailView):
    model = EstatusAspirante
    template_name = 'CandidatosMaestria/results.html'

def asignar(request, estatus_id):
    estatusalumnos = get_object_or_404(EstatusAspirante, pk=estatus_id)
    try:
        selected_aspirante = estatusalumnos.aspirante_set.get(pk=request.POST['aspirante'])
    except (KeyError, Aspirante.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'CandidatosMaestria/detail.html', {
            'estatusalumno': estatusalumnos,
            'error_message': "You didn't select a choice.",
        })
    else:
        nuevoestatus = get_object_or_404(EstatusAspirante, pk=4)
        selected_aspirante.estatusalumno = nuevoestatus
        selected_aspirante.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('CandidatosMaestria:results', args=(estatusalumnos.id,)))

"""
def login(request):
    m = Member.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.id
        return HttpResponse("You're logged in.")
    else:
        return HttpResponse("Your username and password didn't match.")
"""

def Login(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('CandidatosMaestria:index'))
        
    if request.method=='POST':
        if request.user.is_authenticated:
            return render(request, 'CandidatosMaestria/index.html')
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                try:
                    aspirante = Aspirante.objects.get(Usuario=user)
                    
                except Aspirante.DoesNotExist:
                    try:
                        docente = Docente.objects.get(Usuario=user)
                    except Docente.DoesNotExist:
                         logout(request)
                         return render(request,'CandidatosMaestria/Login.html',{'error_message':'La Cuenta No Tiene Accesso'})
                    return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))  
                return HttpResponseRedirect(reverse('CandidatosMaestria:index'))    
            else:
                return render(request,'CandidatosMaestria/Login.html',{'error_message':'Cuenta o Contraseña Equivocada'})
    else:
        return render(request, 'CandidatosMaestria/Login.html')
         
def Registro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('CandidatosMaestria:index'))
    else:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            email= request.POST['email']
            
            try:
                user = authenticate(request, username=username, password=password)
            except IntegrityError:
                return render(request, 'CandidatosMaestria/Registro.html',{'error_message':'El usuario ya Existe'})
            
            
            user = User.objects.create_user(username,email,password)
            statusA = get_object_or_404(EstatusAspirante, pk=1)
            periodoA  = Periodo.objects.order_by('pk').last()

            try:
                aspirante = Aspirante.objects.create(nombre=request.POST['nombre'],apellidopaterno=request.POST['apellidopaterno'],apellidomaterno=request.POST['apellidomaterno'],curp=request.POST['curp'],email=user.email,estatusaspirante=statusA,Usuario=user, periodo=periodoA)
            except 	IntegrityError:
                user.delete()
                return render(request, 'CandidatosMaestria/Registro.html',{'error_message':'El verifique sus informacion'})
             
            return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))

        else:
            return render(request, 'CandidatosMaestria/Registro.html')
        



def index(request):
    if request.user.is_authenticated:

        try:
            aspirante01 = Aspirante.objects.get(Usuario=request.user)
        except Aspirante.DoesNotExist:
            return HttpResponseRedirect(reverse('CandidatosMaestria:Logout'))
        


        ListaRequisitos=DetalleRequisito.objects.filter(aspirante=aspirante01).order_by('id')
        
        # Pendiente para cuando tenga mas tienpo ListaCursosAspirante=list(ChainMap(listaaspirantecurso, listaCurso))
        return render(request,'CandidatosMaestria/index.html',{'aspirante':aspirante01,'ListaRequisitos':ListaRequisitos})
        
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))


def ListarCursos(request):
    if request.user.is_authenticated:
        
        try:
            aspirante01 = Aspirante.objects.get(Usuario=request.user)
        except Aspirante.DoesNotExist:
            return HttpResponseRedirect(reverse('CandidatosMaestria:Logout'))
        
        listaaspirantecurso = DetalleAspiranteCurso.objects.filter(aspirante=aspirante01).order_by('cursopropedeutico')
        

        return render(request,'CandidatosMaestria/ListaCursos.html',{'aspirante':aspirante01,'ListaCurso':listaaspirantecurso})
        
    else:
        return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))



def entrevista(request):
    if request.user.is_authenticated:
        try:
            aspirante01 = Aspirante.objects.get(Usuario=request.user)
        except Aspirante.DoesNotExist:
            return HttpResponseRedirect(reverse('CandidatosMaestria:Logout'))
        
        try:
            entrevista = Entrevista.objects.get(aspirante = aspirante01)
        except Entrevista.DoesNotExist:
            return render(request,'CandidatosMaestria/Entrevista.html',{'aspirante':aspirante01})
        
        return render(request,'CandidatosMaestria/Entrevista.html',{'aspirante':aspirante01,'Entrevista':entrevista})
    else:
        return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))


def UploadFile(request):

    if request.method == "POST":
        
        # Fetching the form data
        if request.FILES:
            fecha=datetime.now()
            requitisoid = request.POST['id']
            ListaRequisitos=get_object_or_404(DetalleRequisito,id=requitisoid)
            status =get_object_or_404(EstatusRequisitoEstudiante,pk=2)
            # Saving the information in the database
            ListaRequisitos.ruta = request.FILES['uploadedFile']
            ListaRequisitos.estatus=status
            ListaRequisitos.carga=fecha
            ListaRequisitos.observaciones=" "
            ListaRequisitos.save()

        else:
            return HttpResponseRedirect(reverse('CandidatosMaestria:index'))

    return HttpResponseRedirect(reverse('CandidatosMaestria:index'))


def Logout(request):
    if request.user.is_authenticated:
        
            logout(request)
            return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))




def Subir(request,requisito_id):
    requisitoAlumno= get_object_or_404(DetalleRequisito,pk=requisito_id)
    return render(request, 'CandidatosMaestria/Archivos.html',{'requisito_id':requisito_id,'Descripcion':requisitoAlumno.requisito.descripcion,'size':(requisitoAlumno.requisito.tamaño * 1000000)})


def Maestro(request):

    if request.user.is_authenticated:

        try:
            docente1 = Docente.objects.get(Usuario=request.user)
        except Docente.DoesNotExist:
            return HttpResponseRedirect(reverse('CandidatosMaestria:Logout'))

        return render(request,'CandidatosMaestria/Maestro.html',{'Docente':docente1})
        
    
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))



def EntrevistasDocente(request):
    if request.user.is_authenticated:

        try:
            docente1 = Docente.objects.get(Usuario=request.user)
        except Docente.DoesNotExist:
            return HttpResponseRedirect(reverse('CandidatosMaestria:Logout'))
        
        

        try:
            listaentrevista = DetalleEntrevista.objects.filter(docente=docente1).order_by('pk')
        except DetalleEntrevista.DoesNotExist:
            return render(request,'CandidatosMaestria/EntrevistasDocentes.html',{'Docente':docente1})

        
        fecha=datetime.now()
        return render(request,'CandidatosMaestria/EntrevistasDocente.html',{'Docente':docente1,'listaentrevista':listaentrevista,'fecha':fecha.date()})

    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))


def CursosDocente(request):
    if request.user.is_authenticated:

        try:
            docente1 = Docente.objects.get(Usuario=request.user)
        except Docente.DoesNotExist:
            return HttpResponseRedirect(reverse('CandidatosMaestria:Logout'))
        

        try:
            listadocentecurso = CursoPropedeutico.objects.filter(docente=docente1).order_by('pk')
        except DetalleEntrevista.DoesNotExist:
            return render(request,'CandidatosMaestria/Maestro.html',{'Docente':docente1})

        return render(request,'CandidatosMaestria/CursosDocentes.html',{'Docente':docente1,'listadocentecurso':listadocentecurso})

    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))




def Curso(request,idCurso):
    if request.user.is_authenticated:
        try:
            docente1 = Docente.objects.get(Usuario=request.user)
        except Docente.DoesNotExist:
            return HttpResponseRedirect(reverse('CandidatosMaestria:Logout'))

        
        try:
            listaalumnocurso = DetalleAspiranteCurso.objects.filter(cursopropedeutico=idCurso).order_by('id')
        except Docente.DoesNotExist:
            return HttpResponseRedirect(reverse('CandidatosMaestria:CursosDocente'))
                
        return render(request,'CandidatosMaestria/CursoModal.html',{'listaalumnocurso':listaalumnocurso})
          

    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))



def CursoSave(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            Cursoid=request.POST['id']

            ListaAlumnos = list(DetalleAspiranteCurso.objects.filter(cursopropedeutico=Cursoid).order_by('pk'))
            if not ListaAlumnos:
                return HttpResponseRedirect(reverse('CandidatosMaestria:CursosDocente'))
            
            for calificacion in ListaAlumnos:
                calificacion.Calificacion=request.POST[str(calificacion.id)]
                calificacion.save()

            return HttpResponseRedirect(reverse('CandidatosMaestria:CursosDocente'))
           
        return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))   

    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))






def SaveEncuesta(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            Encuesta01 = Encuesta.objects.get(pk=request.POST['Encuestaid'])
            listapreguntas = DetalleEncuesta.objects.filter(encuesta=Encuesta01).order_by('pk')
            for pregunta in listapreguntas:
                pregunta.Respuesta=request.POST[str(pregunta.id)]
                pregunta.save()
            Encuesta01.Observaciones=request.POST['observaciones']
            Encuesta01.status= StatusEntrevista.objects.get(pk=2)
            Encuesta01.save()
            return HttpResponseRedirect(reverse('CandidatosMaestria:EntrevistasDocente'))
        return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))





def Encuestas(request,identrevista):
    if request.user.is_authenticated:
            docente1 = Docente.objects.get(Usuario=request.user)
            entrevista =get_object_or_404(DetalleEntrevista,pk=identrevista,docente=docente1)
            

            try:
                Encuesta01 = Encuesta.objects.get(detalleentrevista=entrevista)
            except Encuesta.DoesNotExist:
                return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))
            listapreguntas = DetalleEncuesta.objects.filter(encuesta=Encuesta01).order_by('pk')
            return render(request,'CandidatosMaestria/Encuesta.html',{'Docente':docente1,'listapreguntas':listapreguntas,'entrevista':entrevista,'Encuesta01':Encuesta01.id})
   
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))



def VerEncuesta(request,identrevista):
    if request.user.is_authenticated:
            docente1 = Docente.objects.get(Usuario=request.user)
            entrevista =get_object_or_404(DetalleEntrevista,pk=identrevista,docente=docente1)


            try:
                Encuesta01 = Encuesta.objects.get(detalleentrevista=entrevista)
            except Encuesta.DoesNotExist:
                return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))

            return render(request,'CandidatosMaestria/VerEncuesta.html',{'Docente':docente1,'Encuesta01':Encuesta01,'Entrevistaid':identrevista})
   
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))


def PdfEncuesta(request,identrevista):
    if request.user.is_authenticated:
            docente1 = Docente.objects.get(Usuario=request.user)
            entrevista =get_object_or_404(DetalleEntrevista,pk=identrevista,docente=docente1)


            
            try:
                Encuesta01 = Encuesta.objects.get(detalleentrevista=entrevista)
            except Encuesta.DoesNotExist:
                return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))

            
            data = {'Docente':docente1,'Encuesta01':Encuesta01}

            pdf = render_to_pdf('CandidatosMaestria/VerEncuesta.html',data)
            return HttpResponse(pdf, content_type='application/pdf')
   
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))





def ponencia(request,identrevista):
    if request.user.is_authenticated:
            docente1 = Docente.objects.get(Usuario=request.user)
            entrevista =get_object_or_404(DetalleEntrevista,pk=identrevista,docente=docente1)
            listascriterio= Criterio.objects.order_by('pk') 
            ListaCriterioRubrica = []
            for Criterio01 in listascriterio:
                CriterioRubrica = list(DetalleCriterioRubrica.objects.order_by('pk').filter(criterio=Criterio01))
                if not DetalleCriterioRubrica:
                    raise Http404("No MyModel matches the given query.")
                ListaCriterioRubrica.append(CriterioRubrica)

            try:
                Ponencia01 = Ponencia.objects.get(detalleentrevista=entrevista)
            except Ponencia.DoesNotExist:
                return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))
                
            return render(request,'CandidatosMaestria/Ponencia.html',{'ListaCriterioRubrica':ListaCriterioRubrica,'Docente':docente1,'Ponencia01':Ponencia01.id})
        
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))


def Verponencia(request,identrevista):
    if request.user.is_authenticated:
            docente1 = Docente.objects.get(Usuario=request.user)
            entrevista =get_object_or_404(DetalleEntrevista,pk=identrevista,docente=docente1)
            try:
                Ponencia01 = Ponencia.objects.get(detalleentrevista=entrevista)  
            except Ponencia.DoesNotExist:
                return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))
                
            return render(request,'CandidatosMaestria/VerPonencia.html',{'Docente':docente1,'Ponencia01':Ponencia01,'Entrevistaid':identrevista})
        
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))


def PdfPonencia (request,identrevista):
    if request.user.is_authenticated:
            docente1 = Docente.objects.get(Usuario=request.user)
            entrevista =get_object_or_404(DetalleEntrevista,pk=identrevista,docente=docente1)
            try:
                Ponencia01 = Ponencia.objects.get(detalleentrevista=entrevista)  
            except Ponencia.DoesNotExist:
                return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))
            
            data = {'Docente':docente1,'Ponencia01':Ponencia01}

            pdf = render_to_pdf('CandidatosMaestria/VerPonencia.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))


def SavePonencia(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            Ponencia01 = Ponencia.objects.get(pk=request.POST['Ponenciaid'])
            listaCriterio = DetallePonencia.objects.filter(ponencia=Ponencia01).order_by('pk')
            for criterio01 in listaCriterio:
                criterio01.Valor=request.POST[str(criterio01.criterio)]
                criterio01.save()
            Ponencia01.Observaciones=request.POST['observaciones']
            Ponencia01.status=StatusEntrevista.objects.get(pk=2)
            Ponencia01.save()
            return HttpResponseRedirect(reverse('CandidatosMaestria:EntrevistasDocente'))
        return HttpResponseRedirect(reverse('CandidatosMaestria:Maestro'))
    return HttpResponseRedirect(reverse('CandidatosMaestria:Login'))






