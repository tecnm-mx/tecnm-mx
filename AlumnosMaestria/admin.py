from django.contrib import admin

from .models import  Alumno, Semestre,Requisito,DetalleRequisito,EstatusRequisitoAlumno,Periodo


class DetalleRequisitoAdmin(admin.ModelAdmin):
    list_display=('requisito','alumno','estatusrequisitoalumno','observaciones','ruta')
    list_filter=['alumno','estatusrequisitoalumno']


class RequisitoAdmin(admin.ModelAdmin):
    list_display=('nombre','semestre')
    list_filter=['semestre']

admin.site.register(Semestre)
admin.site.register(Alumno)
admin.site.register(EstatusRequisitoAlumno)
admin.site.register(Requisito,RequisitoAdmin)
admin.site.register(DetalleRequisito,DetalleRequisitoAdmin)
admin.site.register(Periodo)
