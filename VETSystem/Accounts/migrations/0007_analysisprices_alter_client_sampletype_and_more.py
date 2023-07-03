# Generated by Django 4.2.1 on 2023-06-25 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Accounts", "0006_bloodchemistry_bloodparasaite_haematology_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AnalysisPrices",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Haematology", models.IntegerField()),
                ("BIOChemistry", models.IntegerField()),
                ("Intestinalparasites", models.IntegerField()),
                ("BloodParasaite", models.IntegerField()),
                ("All", models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name="client",
            name="sampletype",
            field=models.CharField(
                choices=[
                    ("h", "Haematology"),
                    ("b", "BIOChemistry"),
                    ("i", "Intestinalparasites"),
                    ("p", "BloodParasaite"),
                    ("a", "All"),
                ],
                max_length=1,
            ),
        ),
        migrations.AlterField(
            model_name="useradmin",
            name="gender",
            field=models.CharField(
                choices=[("m", "male"), ("f", "female")], max_length=1
            ),
        ),
    ]