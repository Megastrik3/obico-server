# Generated by Django 4.0.10 on 2024-05-08 12:48

from django.db import migrations, models
import django.db.models.deletion

def update_username(apps, schema_editor):
    User = apps.get_model('app', 'User')
    for user in User.objects.all():
        user.username = f'{user.email}_1'
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('app', '0076_remove_notificationsetting_notify_on_other_print_events'),
    ]

    operations = [
        migrations.CreateModel(
            name='Syndicate',
            fields=[
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sites.site')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AddField(
            model_name='user',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.site'),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('email', 'site')},
        ),
        migrations.RunPython(update_username, migrations.RunPython.noop),
        migrations.RunSQL(
            """
            UPDATE django_site
            SET name = 'localhost:3334', domain = 'localhost:3334'
            WHERE domain = 'example.com';
            """,
            ""
        ),
    ]
