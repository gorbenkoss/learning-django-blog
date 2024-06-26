# Generated by Django 4.2.13 on 2024-06-19 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='postreaction',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment'),
        ),
        migrations.AddField(
            model_name='postreaction',
            name='content_type',
            field=models.CharField(default='post', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postreaction',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
