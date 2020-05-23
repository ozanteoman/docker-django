# Generated by Django 2.2.5 on 2020-04-19 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='cover_image',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='album',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('cover_image', models.URLField(max_length=255, null=True)),
                ('sound_file', models.FileField(null=True, upload_to='')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='song', to='album.Album')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='album', to='album.Artist'),
        ),
    ]