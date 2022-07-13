# Generated by Django 4.0.6 on 2022-07-09 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postdislike',
            options={'verbose_name': 'Дизлайк', 'verbose_name_plural': 'Дизлайки'},
        ),
        migrations.AlterModelOptions(
            name='postlike',
            options={'verbose_name': 'Лайк', 'verbose_name_plural': 'Лайки'},
        ),
        migrations.AlterModelOptions(
            name='postuserview',
            options={'verbose_name': 'Просмотр пользователей на постах', 'verbose_name_plural': 'Просмотры пользователей на постах'},
        ),
        migrations.AddField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postdislike',
            name='disliked_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postlike',
            name='liked_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postuserview',
            name='viewed_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postuserview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
