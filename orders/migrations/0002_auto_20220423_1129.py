# Generated by Django 3.1 on 2022-04-23 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20220419_0917'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='variation',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.Variation'),
        ),
    ]