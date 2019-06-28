# Generated by Django 2.0.13 on 2019-06-28 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hansweb', '0002_auto_20190628_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='author',
        ),
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='deliverer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deliverer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='dimensions',
            field=models.CharField(choices=[(0, 'Fits in a shoebox'), (1, 'Fits in a front seat of a car'), (2, 'Fits in a back seat of a car'), (3, 'Fits in a hatchback or SUV'), (4, 'Fits in a pickup truck')], default='Fits in a pickup truck', max_length=1),
        ),
        migrations.AddField(
            model_name='order',
            name='isPaid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(0, 'WAITING_FOR_DELIVERER'), (1, 'IN_TRANSIT'), (2, 'CLOSED')], default='WAITING_FOR_DELIVERER', max_length=1),
        ),
        migrations.AddField(
            model_name='order',
            name='weight',
            field=models.FloatField(default=0.0),
        ),
    ]