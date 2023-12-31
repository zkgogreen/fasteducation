# Generated by Django 5.0 on 2023-12-25 10:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=224)),
                ('kontak', models.CharField(max_length=224)),
                ('text', models.TextField(blank=True)),
                ('closed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Improve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('what', models.CharField(max_length=224)),
                ('why', models.CharField(max_length=224)),
                ('how', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Artikel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=224)),
                ('title', models.CharField(max_length=224)),
                ('header', models.CharField(default='this is header text of content', max_length=224)),
                ('foto', models.FileField(blank=True, upload_to='article')),
                ('jenis', models.IntegerField(choices=[(0, 'news'), (1, 'tips')], default=0)),
                ('text', models.TextField(blank=True)),
                ('tanggal', models.DateTimeField(auto_now_add=True)),
                ('dibaca', models.IntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_artikel', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default='this-is-slug', max_length=224)),
                ('photo', models.FileField(default='example.jpg', upload_to='event')),
                ('nama', models.CharField(max_length=224)),
                ('hadiah', models.CharField(max_length=224)),
                ('jenis', models.IntegerField(choices=[(0, 'credit'), (1, 'barang'), (2, 'kelas'), (3, 'jabatan')], default=0)),
                ('sponsor', models.CharField(max_length=224)),
                ('peraturan', models.TextField(blank=True)),
                ('mulai', models.DateField(blank=True, null=True)),
                ('selesai', models.DateField(blank=True, null=True)),
                ('by', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_event', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis', models.IntegerField(choices=[(0, 'report'), (1, 'update')], default=0)),
                ('text', models.TextField(blank=True)),
                ('tanggal', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_report', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='file/event')),
                ('done', models.BooleanField(default=False)),
                ('eventname', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='website.event')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_event_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
