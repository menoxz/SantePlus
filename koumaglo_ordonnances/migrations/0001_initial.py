# Generated by Django 4.2 on 2025-05-06 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("koumaglo_parametres", "0001_initial"),
        ("koumaglo_consultations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ordonnance",
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
                ("code_ordonnance", models.CharField(max_length=50, unique=True)),
                ("date_ordonnance", models.DateTimeField()),
                (
                    "consultation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ordonnances",
                        to="koumaglo_consultations.consultation",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ordonnance",
                "verbose_name_plural": "Ordonnances",
            },
        ),
        migrations.CreateModel(
            name="OrdonnanceDetail",
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
                (
                    "code_ordonnance_detail",
                    models.CharField(max_length=50, unique=True),
                ),
                ("posologie_medicament", models.TextField()),
                (
                    "medicament",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="koumaglo_parametres.medicament",
                    ),
                ),
                (
                    "ordonnance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="details",
                        to="koumaglo_ordonnances.ordonnance",
                    ),
                ),
            ],
            options={
                "verbose_name": "Détail Ordonnance",
                "verbose_name_plural": "Détails Ordonnances",
            },
        ),
    ]
