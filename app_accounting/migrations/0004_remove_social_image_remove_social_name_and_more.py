# Generated by Django 4.2.13 on 2024-07-11 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_accounting', '0003_alter_social_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='social',
            name='image',
        ),
        migrations.RemoveField(
            model_name='social',
            name='name',
        ),
        migrations.AlterField(
            model_name='experience',
            name='position',
            field=models.CharField(help_text='\n  <script>\n      function clickMe() {\n          alert(\'i am clicked\')\n      }\n  </script>\n  <div style="color: red" onClick="clickMe()">front-end, back-end for example</div>\n', max_length=255),
        ),
    ]
