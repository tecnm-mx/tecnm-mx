# Generated by Django 4.0 on 2022-02-16 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CandidatosMaestria', '0016_periodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='aspirante',
            name='periodo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CandidatosMaestria.periodo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detalleaspirantecurso',
            name='periodo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CandidatosMaestria.periodo'),
            preserve_default=False,
        ),
    ]
