# Generated by Django 4.0 on 2022-02-17 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AlumnosMaestria', '0002_alter_alumno_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='alumno',
            name='periodo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AlumnosMaestria.periodo'),
        ),
    ]
