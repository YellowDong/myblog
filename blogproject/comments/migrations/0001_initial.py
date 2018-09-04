# Generated by Django 2.1 on 2018-08-16 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0002_auto_20180814_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
                ('author', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=225)),
                ('url', models.URLField(blank=True)),
                ('comment_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
        ),
    ]
