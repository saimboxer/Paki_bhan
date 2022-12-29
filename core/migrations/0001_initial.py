# Generated by Django 4.1 on 2022-10-03 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso_3166_1_a2', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='ISO 3166-1 alpha-2')),
                ('iso_3166_1_a3', models.CharField(blank=True, max_length=3, verbose_name='ISO 3166-1 alpha-3')),
                ('iso_3166_1_numeric', models.CharField(blank=True, max_length=3, verbose_name='ISO 3166-1 numeric')),
                ('printable_name', models.CharField(db_index=True, max_length=128, verbose_name='Country name')),
                ('name', models.CharField(max_length=128, verbose_name='Official name')),
                ('display_order', models.PositiveSmallIntegerField(db_index=True, default=0, help_text='Higher the number, higher the country in the list.', verbose_name='Display order')),
                ('is_shipping_country', models.BooleanField(db_index=True, default=False, verbose_name='Is shipping country')),
            ],
            options={
                'verbose_name': 'country',
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('loc_short_name', models.CharField(max_length=20)),
                ('loc_type', models.CharField(choices=[('STOP', 'Stop'), ('STATION', 'Train Station')], max_length=10)),
                ('long', models.FloatField()),
                ('lat', models.FloatField()),
                ('created_at', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.city')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_number', models.CharField(max_length=100)),
                ('vehicle_type', models.CharField(choices=[('Bus', 'Bus'), ('Train', 'Train'), ('Tram', 'Tram')], default='Bus', max_length=5)),
                ('vhcl_capacity', models.IntegerField()),
                ('is_cyclespace_available', models.BooleanField(default=True)),
                ('is_toilet_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=10)),
                ('est_start_time', models.TimeField()),
                ('created_at', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.route')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_type', models.CharField(choices=[('GEN', 'General'), ('SLPR', 'Sleeper'), ('1AC', '1AC'), ('2AC', '2AC'), ('3AC', '3AC')], max_length=5)),
                ('capacity', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vehicle')),
            ],
            options={
                'verbose_name': 'vehicle class',
                'verbose_name_plural': 'vehicle classes',
            },
        ),
        migrations.CreateModel(
            name='RouteDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.location')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.route')),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('long', models.FloatField()),
                ('lat', models.FloatField()),
                ('created_at', models.DateTimeField()),
                ('created_by', models.CharField(max_length=100)),
                ('updated_at', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.location')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.country'),
        ),
    ]