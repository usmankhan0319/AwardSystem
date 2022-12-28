# Generated by Django 4.0.5 on 2022-07-01 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0003_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(default='')),
            ],
        ),
        migrations.RenameModel(
            old_name='Admin',
            new_name='Account',
        ),
        migrations.DeleteModel(
            name='employee',
        ),
        migrations.AddField(
            model_name='answer',
            name='Accountid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.account'),
        ),
        migrations.AddField(
            model_name='answer',
            name='Qid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Api.questions'),
        ),
    ]
