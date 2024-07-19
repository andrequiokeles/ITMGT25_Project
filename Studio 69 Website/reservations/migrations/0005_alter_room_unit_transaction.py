# Generated by Django 5.0.6 on 2024-07-15 15:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_merge_0002_room_unit_0003_auto_20240715_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='unit',
            field=models.CharField(max_length=10),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.booking')),
            ],
            options={
                'ordering': ['-transaction_date'],
            },
        ),
    ]