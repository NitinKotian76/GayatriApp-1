from django.contrib.auth.models import User, Group
from django.db import migrations

# User should be able to choose the name of the group and assign users to that group
# this can be handeled by use of the django admin Module but this creates a different 
def createGroups(apps,schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='')
    Group.objects.get_or_create(name='')

class Migration(migrations.Migration):
    dependencies = []
    operations = [
            migrations.RunPython(createGroups),
            ]


def assign_user_to_group(user_id,group_name):
    pass
    

