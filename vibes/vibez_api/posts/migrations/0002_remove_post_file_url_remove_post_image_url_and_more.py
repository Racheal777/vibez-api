# Generated by Django 5.1.2 on 2024-10-31 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="file_url",
        ),
        migrations.RemoveField(
            model_name="post",
            name="image_url",
        ),
        migrations.RemoveField(
            model_name="post",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="post",
            name="video_url",
        ),
        migrations.CreateModel(
            name="PostMedia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("media_url", models.URLField()),
                (
                    "media_type",
                    models.CharField(
                        choices=[("image", "Image"), ("video", "Video")], max_length=20
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media",
                        to="posts.post",
                    ),
                ),
            ],
        ),
    ]