# Generated by Django 4.2.2 on 2023-06-23 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MainApp', '0006_transaction_delete_payboxtransaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='recipient_account_number',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='reason',
            new_name='transaction_reference',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='email',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='recipient_bank_code',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='reference',
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]