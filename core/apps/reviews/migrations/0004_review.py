# Generated by Django 5.1.1 on 2024-09-18 13:13

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_token'),
        ('reviews', '0003_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('text', models.TextField()),
                ('score', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, message='оценка не может быть ниже 1'), django.core.validators.MaxValueValidator(10, message='оценка не может быть выше 10')], verbose_name='оценка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='customers.customer')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'constraints': [models.UniqueConstraint(fields=('author', 'title'), name='unique_review')],
            },
        ),
    ]
