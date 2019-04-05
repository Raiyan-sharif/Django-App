# Generated by Django 2.1.5 on 2019-04-04 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('tournament', '0003_auto_20190325_0638'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField()),
                ('is_winner', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.GamePlayer')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.PlayerModel')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='scoring',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tournament.Score'),
            preserve_default=False,
        ),
    ]
