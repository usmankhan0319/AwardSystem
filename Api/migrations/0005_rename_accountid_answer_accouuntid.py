# Generated by Django 4.0.5 on 2022-07-01 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0004_answer_questions_rename_admin_account_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='Accountid',
            new_name='Accouuntid',
        ),
    ]
