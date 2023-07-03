# Generated by Django 4.2.1 on 2023-07-03 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Accounts", "0009_alter_useradmin_username"),
    ]

    operations = [
        migrations.RemoveField(model_name="analysisprices", name="BloodParasaite",),
        migrations.AddField(
            model_name="analysisprices",
            name="BloodParasite",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="analysisprices",
            name="All",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="analysisprices",
            name="BIOChemistry",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="analysisprices",
            name="Haematology",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="analysisprices",
            name="Intestinalparasites",
            field=models.IntegerField(default=0),
        ),
    ]