from django.db import models
from django.db.models.base import Model
from django.dispatch import receiver
import os
from django.db.models.signals import post_delete, pre_save, post_save
from django.contrib.auth.models import User


class Semestre(models.Model):
    semestre=models.CharField(max_length=45, null=False)
    descripcion=models.CharField(max_length=85, null=False)
    def __str__(self):
        return self.semestre


class Periodo(models.Model):
    periodo=models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.periodo

class Alumno(models.Model):
    nombre = models.CharField(max_length=40, null=False)
    apellidopaterno = models.CharField(max_length=45,null=False)
    apellidomaterno = models.CharField(max_length=45,null=False)
    curp= models.CharField(max_length=18,null=False,unique=True)
    email= models.EmailField(unique=True)
    NumeroControl=models.IntegerField(null=False, unique=True)
    alumnosemestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    Usuario= models.OneToOneField(User, on_delete=models.CASCADE)
    periodo=models.ForeignKey(Periodo,on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre + " "+ self.apellidopaterno + " " + self.apellidomaterno

    

class EstatusRequisitoAlumno(models.Model):
    nombre = models.CharField(max_length=45, null=False) 
    descripcion = models.CharField(max_length=85,null=False)
    def __str__(self):
        return self.nombre


class Requisito(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=600, null= False)
    detalle = models.ManyToManyField(Alumno, through='DetalleRequisito')
    tamallo=models.DecimalField(null=False, max_digits=4, decimal_places=2)
    semestre= models.ForeignKey(Semestre, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'Alumnos/user_{0}_{1}/{2}'.format(instance.alumno.Usuario,instance.alumno, filename)

class DetalleRequisito(models.Model):
    ruta = models.FileField(upload_to=user_directory_path ,null=True)
    observaciones = models.CharField(max_length=95,blank=True, null=True)
    carga=models.DateTimeField(blank=True,null=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    requisito = models.ForeignKey(Requisito, on_delete=models.CASCADE)
    estatusrequisitoalumno = models.ForeignKey(EstatusRequisitoAlumno, on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=DetalleRequisito)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Elimina el archivo de directorio si se elimina el objeto correspondiente.
    """
    if instance.ruta:
        if os.path.isfile(instance.ruta.path):
            print("path: ", instance.ruta.path)
            os.remove(instance.ruta.path)



@receiver(models.signals.pre_save, sender=DetalleRequisito)
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






@receiver(post_save, sender=Requisito, dispatch_uid="update_stock_count") 
def update_requisito(sender, instance, **kwargs):


    my_objects = list(DetalleRequisito.objects.filter(requisito=instance))
    if not my_objects:
        statusR = EstatusRequisitoAlumno.objects.get(pk=1)
    
        ListaAlumno = Alumno.objects.all()
        for alumno01 in ListaAlumno:
             detalle = DetalleRequisito.objects.create(alumno=alumno01,requisito=instance,estatusrequisitoalumno=statusR,observaciones=" ")
        detalle.save()     

    post_save.disconnect(update_requisito, sender=Requisito)
    post_save.connect(update_requisito, sender=Requisito)


@receiver(post_save, sender=Alumno, dispatch_uid="update_Alumno_count") 
def New_Alumno(sender, instance, **kwargs):


    my_objects = list(DetalleRequisito.objects.filter(alumno=instance))
    if not my_objects:
        statusR = EstatusRequisitoAlumno.objects.get(pk=1)
    
        ListaRequisitos = Requisito.objects.all()
        for requisitoN in ListaRequisitos:
             detalle = DetalleRequisito.objects.create(alumno=instance,requisito=requisitoN,estatusrequisitoalumno=statusR,observaciones=" ")
        detalle.save()     

    post_save.disconnect(New_Alumno, sender=Alumno)
    post_save.connect(New_Alumno, sender=Alumno)
