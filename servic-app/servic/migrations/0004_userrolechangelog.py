# Generated by Django 5.2.1 on 2025-06-01 18:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servic', '0003_serviceproviderprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoleChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_role', models.CharField(choices=[('common', 'Usuario Común'), ('provider', 'Prestador de Servicios')], max_length=10)),
                ('new_role', models.CharField(choices=[('common', 'Usuario Común'), ('provider', 'Prestador de Servicios')], max_length=10)),
                ('reason', models.TextField()),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('changed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='role_changes_made', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_changes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Registro de cambio de rol',
                'verbose_name_plural': 'Registros de cambios de rol',
                'ordering': ['-changed_at'],
            },
        ),
    ]
