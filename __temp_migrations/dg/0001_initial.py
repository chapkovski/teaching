# Generated by Django 2.2.12 on 2020-11-20 09:37

import dg.models
from django.db import migrations, models
import django.db.models.deletion
import otree.db.idmap
import otree.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dg_group', to='otree.Session')),
            ],
            options={
                'db_table': 'dg_group',
            },
            bases=(models.Model, otree.db.idmap.GroupIDMapMixin),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dg_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'dg_subsession',
            },
            bases=(models.Model, otree.db.idmap.SubsessionIDMapMixin),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_role', otree.db.models.StringField(max_length=10000, null=True)),
                ('norm_belief', dg.models.MyOwnField(null=True, verbose_name='Я считаю, что <span class="alert alert-danger">Отправитель</span> \n        должен отдать Получателю такую долю из \n        100 токенов:')),
                ('norm_expectation', dg.models.MyOwnField(null=True, verbose_name='\n        Я полагаю, что в среднем <span class="alert alert-danger">Получатель</span>  ожидает \n         получить от Отправителя следующее число из 100 токенов:')),
                ('empirical_expectation', dg.models.MyOwnField(null=True, verbose_name='Я думаю, что в среднем <span class="alert alert-danger">Получатель</span> передаст Отправителю\n         следующее число из 100 токенов:')),
                ('decision', dg.models.MyOwnField(null=True, verbose_name='Я передаю отправителю из числа имеющихся у меня 100 токенов\n        :')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dg.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dg_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dg_player', to='otree.Session')),
                ('subsession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dg.Subsession')),
            ],
            options={
                'db_table': 'dg_player',
            },
            bases=(models.Model, otree.db.idmap.PlayerIDMapMixin),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dg.Subsession'),
        ),
    ]
