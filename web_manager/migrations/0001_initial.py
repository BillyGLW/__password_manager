from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='web_manager_password',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='django web based password manager', max_length=254, verbose_name='Site name')),
                ('site_url', models.URLField(verbose_name='Site URL')),
                ('account_name', models.CharField(max_length=254, verbose_name='Account name')),
                ('account_password', models.CharField(max_length=254, verbose_name='Account password')),
            ],
        ),
    ]
