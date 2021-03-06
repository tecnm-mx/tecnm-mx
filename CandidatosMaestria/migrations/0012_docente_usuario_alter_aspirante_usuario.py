# Generated by Django 4.0 on 2022-01-24 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('CandidatosMaestria', '0011_rename_detalleentrevista_entrevista_detalleentrevistas'),
    ]

    operations = [
        migrations.AddField(
            model_name='docente',
            name='Usuario',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aspirante',
            name='Usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
