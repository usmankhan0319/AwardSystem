# Generated by Django 4.0.5 on 2022-07-05 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0005_rename_accountid_answer_accouuntid'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='Accouuntid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.account'),
        ),
    ]
