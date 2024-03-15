# Generated by Django 2.2.28 on 2024-03-14 23:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('api_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('genre', models.CharField(max_length=1000)),
                ('url', models.URLField()),
                ('views', models.IntegerField(default=0)),
                ('ratings', models.IntegerField(default=0)),
                ('poster', models.ImageField(upload_to='media/posters')),
                ('release_date', models.DateField(default=django.utils.timezone.now)),
                ('avg_rating', models.DecimalField(decimal_places=10, default=0.0, max_digits=20, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('slug', models.SlugField(unique=True)),
                ('date_added', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('picture', models.ImageField(default='test_media/R.jpeg', upload_to='media/pfps')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contains', to='CriticCorner.Movie')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has', to='CriticCorner.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000)),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='written_about', to='CriticCorner.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writes', to='CriticCorner.UserProfile')),
            ],
        ),
    ]
