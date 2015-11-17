# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address1', models.CharField(max_length=50)),
                ('address2', models.CharField(max_length=25)),
                ('city', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=2)),
                ('zip', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('max_districts', models.IntegerField()),
                ('address', models.ForeignKey(to='server.Address')),
            ],
        ),
        migrations.CreateModel(
            name='DistrictPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('district', models.ForeignKey(to='server.District')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(max_length=100)),
                ('address', models.ForeignKey(to='server.Address')),
            ],
        ),
        migrations.CreateModel(
            name='LegacyDistrict',
            fields=[
                ('DistrictID', models.AutoField(serialize=False, primary_key=True)),
                ('DistrictName', models.CharField(max_length=100)),
                ('MaxDistricts', models.IntegerField()),
                ('Address', models.CharField(max_length=50)),
                ('City', models.CharField(max_length=25)),
                ('State', models.CharField(max_length=2)),
                ('Zip', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='LegacyDistrictPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DistrictID', models.ForeignKey(to='server.LegacyDistrict')),
            ],
        ),
        migrations.CreateModel(
            name='LegacyGroup',
            fields=[
                ('GroupID', models.AutoField(serialize=False, primary_key=True)),
                ('GroupName', models.CharField(max_length=100)),
                ('WebSite', models.URLField(max_length=100)),
                ('Address', models.CharField(max_length=50)),
                ('City', models.CharField(max_length=25)),
                ('State', models.CharField(max_length=2)),
                ('Zip', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='LegacyPosition',
            fields=[
                ('PositionID', models.AutoField(serialize=False, primary_key=True)),
                ('PositionName', models.CharField(max_length=100)),
                ('Description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='legacydistrictposition',
            name='PositionID',
            field=models.ForeignKey(to='server.LegacyPosition'),
        ),
        migrations.AddField(
            model_name='legacydistrict',
            name='GroupID',
            field=models.ForeignKey(to='server.LegacyGroup'),
        ),
        migrations.AddField(
            model_name='legacydistrict',
            name='positions',
            field=models.ManyToManyField(to='server.LegacyPosition', through='server.LegacyDistrictPosition'),
        ),
        migrations.AddField(
            model_name='districtposition',
            name='position',
            field=models.ForeignKey(to='server.Position'),
        ),
        migrations.AddField(
            model_name='district',
<<<<<<< HEAD
            name='group',
            field=models.ForeignKey(blank=True, to='server.Group', null=True),
        ),
        migrations.AddField(
            model_name='district',
=======
>>>>>>> b0b7fe41150205cb03c431c166e06846df517c38
            name='positions',
            field=models.ManyToManyField(to='server.Position', through='server.DistrictPosition'),
        ),
    ]
