# Generated by Django 3.0.6 on 2020-05-12 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0003_auto_20200512_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratings',
            name='purchaseOrderDetailsId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.PurchaseOrderDetails', unique=True),
        ),
    ]
