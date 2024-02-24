# Generated by Django 4.2.10 on 2024-02-23 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_college_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='college',
            name='phone',
        ),
        migrations.CreateModel(
            name='TeamCaptain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.college')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sport')),
            ],
        ),
    ]