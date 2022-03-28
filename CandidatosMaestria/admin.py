from django.contrib import admin

from .models import EstatusAspirante,Aspirante,EstatusRequisitoEstudiante,Requisito,DetalleRequisito, Docente,Entrevista,DetalleEntrevista,CursoPropedeutico,DetalleAspiranteCurso,ExamenSeneval, CatalogoPregunta,Encuesta,DetalleEncuesta,Criterio,Rubrica,DetalleCriterioRubrica,Ponencia,DetallePonencia,CatalogoMaterias,StatusEntrevista,Periodo

class ExamenSenevalAdmin(admin.ModelAdmin):
    list_display=('aspirante','ICNE','PMA','PAN','ELE','CLE','MET','ICL','IUG')

class ExamenSenevalline(admin.StackedInline):
    model=ExamenSeneval
    
class DetalleRequisitoline(admin.StackedInline):
    model=DetalleRequisito

class DetalleAspiranteCursoline(admin.StackedInline):
    model=DetalleAspiranteCurso

class AspiranteAdmin(admin.ModelAdmin):
    
    list_display = ('nombre','apellidopaterno','apellidomaterno','curp','email','estatusaspirante')
    inlines= [ExamenSenevalline]


class DocenteAdmin(admin.ModelAdmin):

    list_display = ('Nombre','ApellidoPaterno','ApellidoMaterno','Curp','Rfc','CedulaProfesional','Email')


class EstatusAspiranteAdmin(admin.ModelAdmin):

    list_display=('estatus','descripcion')

class DetalleEntrevistaline(admin.StackedInline):
    model=DetalleEntrevista
class DetalleEncuestaline(admin.StackedInline):
    model=DetalleEncuesta
class CatalogoPreguntaAdmin(admin.ModelAdmin):
    list_display=('Pregunta','descripcion')


class EncuestaAdmin(admin.ModelAdmin):
    inlines = [DetalleEncuestaline]

class EntrevistaAdmin(admin.ModelAdmin):
    list_display=('aspirante','Fecha','HoraInicio')
    inlines= [DetalleEntrevistaline]

class DetalleRequisitoAdmin(admin.ModelAdmin):
    list_display=('requisito','observaciones','estatus','aspirante','ruta')
    list_filter=['aspirante','estatus']

class DetalleRequisitolineAdmin(admin.ModelAdmin):
    list_display=('Clave','FechaInicio','HoraInicio','docente')

class CursoprodeuticoAdmin(admin.ModelAdmin):
    list_display=('Clave','docente','FechaInicio','FechaFinalizacion','HoraInicio','HoraFinalizacion')
    list_filter=['docente','Clave']
    inlines=[DetalleAspiranteCursoline]

class DetalleCriterioRubricaAdmin(admin.ModelAdmin):
    list_display=('criterio','rubrica','valor','Descripcion')
    list_filter=['criterio','rubrica']

class DetalleAspiranteCursoAdmin(admin.ModelAdmin):
     list_display=('aspirante','cursopropedeutico','Calificacion')
     list_filter=['aspirante','cursopropedeutico']

class DetalleEntrevistaAdmin(admin.ModelAdmin):
    list_filter=['docente','entrevista']

class DetallePonenciaAdmin(admin.ModelAdmin):
    list_display=('criterio','Valor')
    list_filter=['ponencia']

class DetallePonecialine(admin.StackedInline):
    model=DetallePonencia

class PonenciaAdmin(admin.ModelAdmin):
    list_display=('detalleentrevista','FechaHora')
    inlines=[DetallePonecialine]


admin.site.register(EstatusAspirante,EstatusAspiranteAdmin)
admin.site.register(Aspirante,AspiranteAdmin)
admin.site.register(EstatusRequisitoEstudiante)
admin.site.register(Requisito)
admin.site.register(DetalleRequisito,DetalleRequisitoAdmin)
admin.site.register(Docente,DocenteAdmin)
admin.site.register(Entrevista,EntrevistaAdmin)
admin.site.register(DetalleEntrevista,DetalleEntrevistaAdmin)
admin.site.register(CursoPropedeutico,CursoprodeuticoAdmin)
admin.site.register(DetalleAspiranteCurso,DetalleAspiranteCursoAdmin)
admin.site.register(ExamenSeneval,ExamenSenevalAdmin)
admin.site.register(CatalogoPregunta,CatalogoPreguntaAdmin)
admin.site.register(Encuesta,EncuestaAdmin)
admin.site.register(DetalleEncuesta)

admin.site.register(Criterio)
admin.site.register(Rubrica)
admin.site.register(DetalleCriterioRubrica,DetalleCriterioRubricaAdmin)
admin.site.register(Ponencia,PonenciaAdmin)
admin.site.register(DetallePonencia,DetallePonenciaAdmin)
admin.site.register(CatalogoMaterias)
admin.site.register(StatusEntrevista)
admin.site.register(Periodo)
