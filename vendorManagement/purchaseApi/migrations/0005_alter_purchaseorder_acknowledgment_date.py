# Generated by Django 4.2.7 on 2023-11-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchaseApi', '0004_alter_purchaseorder_acknowledgment_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='acknowledgment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]