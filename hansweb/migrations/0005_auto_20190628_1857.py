# Generated by Django 2.0.13 on 2019-06-28 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hansweb', '0004_auto_20190628_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=10)),
                ('zip_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='deliveryAddress',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='deliveryAddress', to='hansweb.Address'),
        ),
        migrations.AddField(
            model_name='order',
            name='pickupAddress',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='pickupAddress', to='hansweb.Address'),
        ),
    ]