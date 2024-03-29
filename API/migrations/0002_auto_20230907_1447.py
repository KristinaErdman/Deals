# Generated by Django 3.2.5 on 2023-09-07 14:47

from django.db import migrations, models


def save_old_customer_username(apps, schema_editor):
    Deal = apps.get_model("API", "Deal")
    for deal in Deal.objects.all():
        deal.old_customer_username = deal.customer_id
        deal.save(update_fields=('old_customer_username',))


def save_customer_id(apps, schema_editor):
    Deal = apps.get_model("API", "Deal")
    Customer = apps.get_model("API", "Customer")
    for deal in Deal.objects.all():
        deal.customer = Customer.objects.get(username=deal.old_customer_username)
        deal.save()


class Migration(migrations.Migration):
    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deal',
            name='old_customer_username',
            field=models.CharField(max_length=50, null=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='логин покупателя'),
        ),
        migrations.RunPython(save_old_customer_username),
        migrations.RemoveField(
            model_name='deal',
            name='customer',
        ),
        migrations.AddField(
            model_name='deal',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=models.deletion.CASCADE, related_name='deals',
                                    to='API.customer'),
        ),
        migrations.RunPython(save_customer_id),
        migrations.RemoveField(
            model_name='deal',
            name='old_customer_username',
        ),
        migrations.AlterField(
            model_name='deal',
            name='customer',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='deals',
                                    to='API.customer'),
            preserve_default=False,
        ),
    ]
