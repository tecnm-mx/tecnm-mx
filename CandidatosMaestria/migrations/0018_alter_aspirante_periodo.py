# Generated by Django 4.0 on 2022-02-16 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CandidatosMaestria', '0017_aspirante_periodo_detalleaspirantecurso_periodo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aspirante',
            name='periodo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CandidatosMaestria.periodo'),
        ),
    ]
