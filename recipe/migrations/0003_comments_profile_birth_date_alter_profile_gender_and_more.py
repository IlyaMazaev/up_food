# Generated by Django 4.0.2 on 2022-02-27 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_profile_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_id', models.IntegerField()),
                ('comment_text', models.TextField(max_length=150)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(default='1990-01-01'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Мужчина'), ('F', 'Женщина'), ('NS', 'Не указано')], default='NS', max_length=4),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to=''),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_text', models.TextField(max_length=150)),
                ('likes', models.IntegerField(default=0)),
                ('comments', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recipe.comments')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recipe.profile')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.profile'),
        ),
    ]
