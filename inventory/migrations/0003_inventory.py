# Generated by Django 5.1.1 on 2024-10-14 19:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('quantity_in_stock', models.PositiveBigIntegerField(default=0)),
                ('quantity_sold', models.PositiveBigIntegerField(default=0)),
                ('buy_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sell_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_bought', models.DateField()),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('stock_alert', models.PositiveBigIntegerField(default=15)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.category')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.unit')),
            ],
        ),
    ]
