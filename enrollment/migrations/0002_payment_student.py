from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enrollment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=models.deletion.DO_NOTHING,
                to="enrollment.studentinfo",
            ),
        ),
    ]
