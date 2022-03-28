from enum import unique
from pyexpat import model
from xml.dom.minidom import Document
from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.dispatch import receiver
import os
from django.db.models.signals import post_delete, pre_save, post_save
from django.contrib.auth.models import User
from datetime import datetime

from django.http import Http404



class StatusEntrevista(models.Model):
    Estatus=models.CharField(max_length=45, null=False)
    Descripcion=models.CharField(max_length=85, blank=True, null=True)

    def __str__(self):
        return self.Estatus


class Periodo(models.Model):
    periodo=models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.periodo



class EstatusAspirante(models.Model):
    estatus=models.CharField(max_length=45, null=False)
    descripcion=models.CharField(max_length=85, null=False)

    def __str__(self):
        return self.estatus

class Aspirante(models.Model):
    idaspirante= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40, null=False)
    apellidopaterno = models.CharField(max_length=45,null=False)
    apellidomaterno = models.CharField(max_length=45,null=False)
    curp= models.CharField(max_length=18,null=False,unique=True)
    email= models.EmailField(unique=True)
    estatusaspirante = models.ForeignKey(EstatusAspirante, on_delete=models.CASCADE)
    Usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    periodo=models.ForeignKey(Periodo,on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre + " "+ self.apellidopaterno + " " + self.apellidomaterno



class ExamenSeneval(models.Model):
    ICNE = models.IntegerField(null=False)
    PMA = models.IntegerField(null=False)
    PAN = models.IntegerField(null=False)
    ELE = models.IntegerField(null=False)
    CLE = models.IntegerField(null=False)
    MET = models.IntegerField(null=False)
    ICL = models.IntegerField(null=False)
    IUG = models.IntegerField(null=False)
    aspirante = models.OneToOneField(Aspirante, on_delete=models.CASCADE)

class EstatusRequisitoEstudiante(models.Model):
    nombre = models.CharField(max_length=45, null=False) 
    descripcion = models.CharField(max_length=85,null=False)
    def __str__(self):
        return self.nombre



class Requisito(models.Model):
    nombre = models.CharField(max_length=90, null=False)
    descripcion = models.CharField(max_length=300, null= False)
    detalle = models.ManyToManyField(Aspirante, through='DetalleRequisito')
    tamaño=models.DecimalField(null=False, max_digits=4, decimal_places=2)
    def __str__(self):
        return self.nombre
    

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'Aspirantes/user_{0}_{1}/{2}'.format(instance.aspirante.Usuario,instance.aspirante, filename)

class DetalleRequisito(models.Model):
    aspirante = models.ForeignKey(Aspirante, on_delete=models.CASCADE)
    requisito = models.ForeignKey(Requisito, on_delete=models.CASCADE)
    ruta = models.FileField(upload_to=user_directory_path ,null=True,blank=True)
    carga=models.DateTimeField(blank=True,null=True)
    observaciones = models.CharField(max_length=85,blank=True, null=True)
    estatus = models.ForeignKey(EstatusRequisitoEstudiante, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.aspirante) + str(self.requisito)


@receiver(post_delete, sender=DetalleRequisito)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Elimina el archivo de directorio si se elimina el objeto correspondiente.
    """
    if instance.ruta:
        if os.path.isfile(instance.ruta.path):
            print("path: ", instance.ruta.path)
            os.remove(instance.ruta.path)



@receiver(pre_save, sender=DetalleRequisito)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Elimina el archivo antiguo del directorio cuando se actualiza el objeto correspondiente con un nuevo archivo
    """
    if not instance.pk:
        return False

    old_file = sender.objects.get(pk=instance.pk).ruta

    if old_file:
        new_file = instance.ruta
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    else:
        pass



class Docente(models.Model):
    Nombre = models.CharField(max_length=45,null = False)
    ApellidoPaterno= models.CharField(max_length=45,null=False)
    ApellidoMaterno= models.CharField(max_length=45,null=False)
    Curp= models.CharField(max_length=18, null=False, unique=True)
    Rfc=models.CharField(max_length=13,null=False, unique=True)
    CedulaProfesional = models.CharField(max_length=8, null=False, unique=True)
    Email = models.EmailField(null=False, unique=True)
    Usuario=models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.Nombre + " "+ self.ApellidoPaterno + " " + self.ApellidoMaterno


class Entrevista(models.Model):
    Fecha = models.DateField()
    HoraInicio = models.TimeField()
    HoraFinal = models.TimeField()
    Observaciones = models.CharField(max_length=45,blank=True, null=True)
    aspirante= models.OneToOneField(Aspirante, on_delete=models.CASCADE)
    detalleentrevistas = models.ManyToManyField(Docente,through='DetalleEntrevista')
    def __str__(self):
        return str(self.aspirante) + '--'+ str(self.Fecha) 

class DetalleEntrevista(models.Model):
    entrevista = models.ForeignKey(Entrevista, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('entrevista', 'docente'),)
        indexes = [
            models.Index(fields=['entrevista', 'docente']),
        ]

    def __str__(self):
        return str(self.docente)+" -- "+str(self.entrevista)




class CatalogoMaterias(models.Model):
    idMateria=models.AutoField(primary_key=True)
    Materia=models.CharField(max_length=100,null=False)
    Descripcion=models.CharField(max_length=400,null=False)

    def __str__(self):
        return self.Materia



class CursoPropedeutico(models.Model):
    idcurso= models.AutoField(primary_key=True)
    Clave = models.ForeignKey(CatalogoMaterias, on_delete=models.CASCADE)
    FechaInicio= models.DateField()
    FechaFinalizacion= models.DateField()
    HoraInicio= models.TimeField()
    HoraFinalizacion = models.TimeField()
    docente = models.ForeignKey(Docente,on_delete=models.CASCADE)
    periodo=models.ForeignKey(Periodo,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Clave) +"  "+ str(self.docente)
    



class DetalleAspiranteCurso(models.Model):
    id= models.AutoField(primary_key=True)
    aspirante = models.ForeignKey(Aspirante, on_delete=models.CASCADE)
    cursopropedeutico = models.ForeignKey(CursoPropedeutico, on_delete=models.CASCADE)
    Calificacion= models.IntegerField(null=False)
    
    class Meta:
        unique_together = (('aspirante', 'cursopropedeutico'),)
        indexes = [
            models.Index(fields=['aspirante', 'cursopropedeutico']),
        ]

 






class CatalogoPregunta(models.Model):
    Pregunta= models.CharField(max_length=200, null=False)
    descripcion = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.Pregunta


def user_directory_path2(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'Entrevista/Encuesta/{0}_{1}/{2}'.format(instance.pk,instance.detalleentrevista, filename)


class Encuesta(models.Model):
    FechaHora=models.DateTimeField(blank=True,null=True)
    Observaciones= models.CharField(max_length=100,blank=True, null=True)
    detalleentrevista= models.ForeignKey(DetalleEntrevista,on_delete=models.CASCADE, unique=True)
    Documento = models.FileField(upload_to=user_directory_path2 ,null=True,blank=True)
    detalleEncuesta = models.ManyToManyField(CatalogoPregunta, through='DetalleEncuesta')
    status = models.ForeignKey(StatusEntrevista, on_delete=models.CASCADE)


@receiver(post_delete, sender=Encuesta)
def auto_delete_file_on_delete2(sender, instance, **kwargs):
    """
    Elimina el archivo de directorio si se elimina el objeto correspondiente.
    """
    if instance.Documento:
        if os.path.isfile(instance.Documento.path):
            print("path: ", instance.Documento.path)
            os.remove(instance.Documento.path)



@receiver(pre_save, sender=Encuesta)
def auto_delete_file_on_change2(sender, instance, **kwargs):
    """
    Elimina el archivo antiguo del directorio cuando se actualiza el objeto correspondiente con un nuevo archivo
    """
    if not instance.pk:
        return False

    old_file = sender.objects.get(pk=instance.pk).Documento

    if old_file:
        new_file = instance.Documento
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    else:
        pass




class DetalleEncuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    catalogopreguntas = models.ForeignKey(CatalogoPregunta, on_delete=models.CASCADE)
    Respuesta = models.CharField(max_length=150,blank=True, null=True)



class Criterio(models.Model):
    Criterio=models.CharField(max_length=50,null=False)


    def __str__(self):
        return self.Criterio
    

class Rubrica(models.Model):
    Rubrica=models.CharField(max_length=50,null=False)
    detallecriteriorubricas = models.ManyToManyField(Criterio, through='DetalleCriterioRubrica')
    
    def __str__(self):
        return self.Rubrica



class DetalleCriterioRubrica(models.Model):
    criterio=models.ForeignKey(Criterio,on_delete=models.CASCADE)
    rubrica=models.ForeignKey(Rubrica,on_delete=models.CASCADE)
    valor= models.IntegerField(null=False)
    Descripcion = models.CharField(max_length=100,null=False)
    class Meta:
        unique_together = (('criterio', 'rubrica'),)
        indexes = [
            models.Index(fields=['criterio', 'rubrica']),
        ]


def user_directory_path3(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'Entrevista/Ponencia/{0}_{1}/{2}'.format(instance.pk,instance.detalleentrevista, filename)


class Ponencia(models.Model):
    FechaHora=models.DateTimeField(blank=True,null=True)
    Observaciones= models.CharField(max_length=100,blank=True, null=True)
    detalleentrevista= models.ForeignKey(DetalleEntrevista,on_delete=models.CASCADE,unique=True)
    Documento = models.FileField(upload_to=user_directory_path3,null=True,blank=True)
    detallePonencia = models.ManyToManyField(Criterio, through='DetallePonencia')
    status = models.ForeignKey(StatusEntrevista, on_delete=models.CASCADE)


@receiver(post_delete, sender=Ponencia)
def auto_delete_file_on_delete3(sender, instance, **kwargs):
    """
    Elimina el archivo de directorio si se elimina el objeto correspondiente.
    """
    if instance.Documento:
        if os.path.isfile(instance.Documento.path):
            print("path: ", instance.Documento.path)
            os.remove(instance.Documento.path)



@receiver(pre_save, sender=Ponencia)
def auto_delete_file_on_change3(sender, instance, **kwargs):
    """
    Elimina el archivo antiguo del directorio cuando se actualiza el objeto correspondiente con un nuevo archivo
    """
    if not instance.pk:
        return False

    old_file = sender.objects.get(pk=instance.pk).Documento

    if old_file:
        new_file = instance.Documento
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    else:
        pass


class DetallePonencia(models.Model):
    ponencia=models.ForeignKey(Ponencia,on_delete=models.CASCADE)
    criterio=models.ForeignKey(Criterio,on_delete=models.CASCADE)
    Valor=models.IntegerField(null=True)
    
    





@receiver(post_save, sender=Requisito, dispatch_uid="update_stock_count") 
def update_requisito(sender, instance, **kwargs):


    my_objects = list(DetalleRequisito.objects.filter(requisito=instance))
    if not my_objects:
        statusR = EstatusRequisitoEstudiante.objects.get(pk=1)
    
        ListaAspirante = Aspirante.objects.all()
        for aspirante in ListaAspirante:
             detalle = DetalleRequisito.objects.create(aspirante=aspirante,requisito=instance,estatus=statusR,observaciones=" ")
        detalle.save()     

    post_save.disconnect(update_requisito, sender=Requisito)
    post_save.connect(update_requisito, sender=Requisito)



@receiver(post_save, sender=Criterio, dispatch_uid="update_stock_count") 
def update_Criterio(sender, instance, **kwargs):


    my_objects = list(DetalleCriterioRubrica.objects.filter(criterio=instance))
    if not my_objects:
        
        ListaRubrica = Rubrica.objects.all()
        for rubricaN in ListaRubrica:
             detalle = DetalleCriterioRubrica.objects.create(criterio=instance,rubrica=rubricaN,Descripcion="----", valor=0)

        
        ListaPonencia=Ponencia.objects.all()
        for PonenciaN in ListaPonencia:
            detalle2= DetallePonencia.objects.create(ponencia=PonenciaN, criterio=instance)
            
        detalle.save()     

    post_save.disconnect(update_Criterio, sender=Criterio)
    post_save.connect(update_Criterio, sender=Criterio)


@receiver(post_save, sender=Rubrica, dispatch_uid="update_stock_count") 
def update_Rubrica(sender, instance, **kwargs):


    my_objects = list(DetalleCriterioRubrica.objects.filter(rubrica=instance))
    if not my_objects:
        
        ListaCriterio = Criterio.objects.all()
        for CriterioN in ListaCriterio:
             detalle = DetalleCriterioRubrica.objects.create(criterio=CriterioN,rubrica=instance,Descripcion="----", valor=0)
        detalle.save()     

    post_save.disconnect(update_Rubrica, sender=Rubrica)
    post_save.connect(update_Rubrica, sender=Rubrica)





@receiver(post_save, sender=Aspirante, dispatch_uid="update_stock_count") 
def update_Aspirante(sender, instance, **kwargs):


    my_objects = list(DetalleRequisito.objects.filter(aspirante=instance))
    if not my_objects:
        statusR = EstatusRequisitoEstudiante.objects.get(pk=1)
    
        ListaRequisitos = Requisito.objects.all()
        for requisitoN in ListaRequisitos:
             detalle = DetalleRequisito.objects.create(aspirante=instance,requisito=requisitoN,estatus=statusR,observaciones=" ")
        detalle.save()     

    post_save.disconnect(update_Aspirante, sender=Aspirante)
    post_save.connect(update_Aspirante, sender=Aspirante)



@receiver(post_save, sender=CatalogoPregunta, dispatch_uid="update_stock_count") 
def update_CatalogoPregunta(sender, instance, **kwargs):


    my_objects = list(DetalleEncuesta.objects.filter(catalogopreguntas=instance))
    if not my_objects:
        ListaEncuesta = Encuesta.objects.all()
        for encuestaN in ListaEncuesta:
             detalle = DetalleEncuesta.objects.create(encuesta=encuestaN,catalogopreguntas=instance,Respuesta=" ")
        detalle.save()     

    post_save.disconnect(update_CatalogoPregunta, sender=CatalogoPregunta)
    post_save.connect(update_CatalogoPregunta, sender=CatalogoPregunta)







@receiver(post_save, sender=DetalleEntrevista, dispatch_uid="update_stock_count2") 
def update_stock(sender, instance, **kwargs):
    try:
        Encuesta01 = Encuesta.objects.get(detalleentrevista=instance)
    except Encuesta.DoesNotExist:

        try:
             estatus = StatusEntrevista.objects.get(pk=1)
        except:
            raise Http404("No MyModel matches the given query.")

        fecha=datetime.now()           
        Encuesta01 = Encuesta.objects.create(FechaHora=fecha,detalleentrevista=instance,Observaciones=" ",status=estatus)
        

        ListaPreguntas = CatalogoPregunta.objects.all()
                 
        for pregunta in ListaPreguntas:
            detalle = DetalleEncuesta.objects.create(encuesta=Encuesta01,catalogopreguntas=pregunta,Respuesta=" ")
        
        Ponencia01 = Ponencia.objects.create(FechaHora=fecha,detalleentrevista=instance,Observaciones=" ",status=estatus)
        
        ListaCriterio = Criterio.objects.order_by('pk')
        for criterio01 in ListaCriterio:
            detalle2 = DetallePonencia.objects.create(ponencia=Ponencia01,criterio=criterio01)


        Encuesta01.save()       

        
    post_save.disconnect(update_stock, sender=DetalleEntrevista)
    post_save.connect(update_stock, sender=DetalleEntrevista)




















