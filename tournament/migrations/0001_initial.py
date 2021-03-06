# Generated by Django 2.1.5 on 2019-04-04 10:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GamePlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_invited', models.BooleanField(default=False)),
                ('match_accepted', models.BooleanField(default=False)),
                ('match_ended', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.PlayerModel')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_date', models.DateTimeField(auto_now_add=True)),
                ('race_to', models.IntegerField()),
                ('game_type', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=20)),
                ('game_mode', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=20)),
                ('playing_with', models.ManyToManyField(to='tournament.GamePlayer')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.ClubModel')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tornament_name', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='tournament_poster/')),
                ('creation_date', models.DateField(default=datetime.date.today, editable=False)),
                ('is_accepted', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('capacity', models.PositiveIntegerField()),
                ('enrty_fee_with_per_hour_charge', models.PositiveIntegerField()),
                ('zone_location', models.CharField(max_length=100)),
                ('category_type', models.CharField(max_length=100)),
                ('tournament_type', models.CharField(max_length=100)),
                ('prize_worth', models.CharField(max_length=255)),
                ('host_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='host', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
