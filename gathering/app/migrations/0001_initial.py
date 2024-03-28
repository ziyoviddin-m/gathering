# Generated by Django 5.0.3 on 2024-03-28 08:42

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
            name='Collect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('occasion', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('planned_amount', models.PositiveIntegerField()),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='collect_covers/')),
                ('end_datetime', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.PositiveIntegerField()),
                ('date_time_payment', models.DateTimeField(auto_now_add=True)),
                ('collect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='app.collect')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]