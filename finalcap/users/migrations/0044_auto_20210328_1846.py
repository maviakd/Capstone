# Generated by Django 2.2.16 on 2021-03-28 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0043_auto_20210328_0420'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='ivk',
            name='iv',
            field=models.TextField(default=b'\xc5\xec\x8e\x1f\x85A\x84\x9a\xef\x8d\xd8\x1b\xe7\xa4\xb7\x95K\xbd\xb2\xc4wd\x8f\xe7\xc5\xa4\xc5Z\x18[\x9d\xa4'),
        ),
    ]
