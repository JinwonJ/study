# Generated by Django 3.2.9 on 2021-12-16 01:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('fake_account', models.BooleanField(default=False)),
                ('last_notification_read_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(max_length=32, unique=True)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('following', models.ManyToManyField(related_name='followers', to='users.User')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ImageField(blank=True, upload_to='images/%Y/%m/%d/')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('image', models.ImageField(blank=True, upload_to='images/%Y/%m/%d/')),
                ('location', models.CharField(blank=True, max_length=100)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('website', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
