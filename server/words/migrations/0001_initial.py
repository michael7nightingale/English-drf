# Generated by Django 4.2.2 on 2023-06-29 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=150, verbose_name='Слово')),
                ('translate', models.CharField(max_length=200, verbose_name='Перевод')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.category')),
            ],
        ),
    ]
