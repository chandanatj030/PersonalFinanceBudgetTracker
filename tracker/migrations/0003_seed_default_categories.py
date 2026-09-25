from django.db import migrations


def create_default_categories(apps, schema_editor):
    Category = apps.get_model('tracker', 'Category')

    categories = [
        'Salary',
        'Food',
        'Travel',
        'Shopping',
        'Bills',
    ]

    for name in categories:
        Category.objects.get_or_create(name=name)


def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('tracker', 'Category')

    Category.objects.filter(
        name__in=[
            'Salary',
            'Food',
            'Travel',
            'Shopping',
            'Bills',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_alter_budget_id_alter_category_id_and_more'),
    ]

    operations = [
        migrations.RunPython(
            create_default_categories,
            remove_default_categories
        ),
    ]