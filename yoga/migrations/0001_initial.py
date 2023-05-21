# Generated by Django 4.0.5 on 2023-03-17 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Title', max_length=300)),
                ('low', models.CharField(default='Low Title', max_length=300)),
                ('info', models.CharField(default='Marka İsimi', max_length=300)),
                ('image', models.ImageField(blank=True, upload_to='products/%y/%m/%d', verbose_name='Resim : (520x666)')),
                ('link', models.CharField(default='Yönlendirilicek URL', max_length=3000)),
            ],
        ),
    ]
