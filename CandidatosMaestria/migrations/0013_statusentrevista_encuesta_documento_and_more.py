# Generated by Django 4.0 on 2022-01-25 19:43

import CandidatosMaestria.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CandidatosMaestria', '0012_docente_usuario_alter_aspirante_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusEntrevista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Estatus', models.CharField(max_length=45)),
                ('Descripcion', models.CharField(blank=True, max_length=85, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='encuesta',
            name='Documento',
            field=models.FileField(blank=True, null=True, upload_to=CandidatosMaestria.models.user_directory_path2),
        ),
        migrations.AddField(
            model_name='ponencia',
            name='Documento',
            field=models.FileField(blank=True, null=True, upload_to=CandidatosMaestria.models.user_directory_path3),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CandidatosMaestria.statusentrevista'),
        ),
        migrations.AddField(
            model_name='ponencia',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CandidatosMaestria.statusentrevista'),
        ),
    ]
