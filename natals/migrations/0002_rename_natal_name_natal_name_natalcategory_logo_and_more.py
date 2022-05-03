# Generated by Django 4.0.4 on 2022-05-03 04:21

from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('praiseres', '0001_initial'),
        ('natals', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='natal',
            old_name='natal_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='natalcategory',
            name='logo',
            field=models.ImageField(blank=True, upload_to=utils.get_file_path),
        ),
        migrations.AlterField(
            model_name='natal',
            name='praiser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_natals', to='praiseres.praiser'),
        ),
    ]
