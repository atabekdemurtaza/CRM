# Generated by Django 4.0.6 on 2022-08-17 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0006_alter_lead_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile'),
            preserve_default=False,
        ),
    ]
