# Generated by Django 3.2.7 on 2021-12-02 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('work_start', models.TimeField()),
                ('work_end', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Operation_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ICD_code', models.CharField(max_length=200)),
                ('cost', models.IntegerField()),
                ('is_difficult', models.BooleanField()),
                ('duration', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('PESEL', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('start', models.TimeField()),
                ('medic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.medic')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.room')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.operation_type')),
            ],
        ),
        migrations.CreateModel(
            name='NonAvailabilityRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.room')),
            ],
        ),
        migrations.CreateModel(
            name='NonAvailabilityMedic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('medic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.medic')),
            ],
        ),
    ]
