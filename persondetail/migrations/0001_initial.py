# Generated by Django 2.1.5 on 2019-04-04 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tournament', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerinstance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.PlayerModel')),
                ('tounament_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.Tournament')),
            ],
        ),
    ]