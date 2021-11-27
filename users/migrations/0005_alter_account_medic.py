# Generated by Django 3.2.7 on 2021-11-27 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        ('users', '0004_alter_account_medic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='medic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.medic'),
        ),
    ]
