from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from bazdidkhodro.models import Image


def AddGroups(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(Image)
    per_view_image = Permission.objects.create(codename='view_image', name='Can View Image', content_type=content_type)
    per_add_image = Permission.objects.create(codename='add_image', name='Can Add Image', content_type=content_type)
    per_change_image = Permission.objects.create(codename='change_image', name='Can Change Image', content_type=content_type)
    per_delete_image = Permission.objects.create(codename='delete_image', name='Can Delete Image', content_type=content_type)

    gr_visitor = Group.objects.create(name='visitor')
    gr_employee = Group.objects.create(name='employee')
    #gr_customer = Group.objects.create(name='customer')

    gr_visitor.permissions.add(per_add_image)
    gr_visitor.permissions.add(per_change_image)
    gr_visitor.permissions.add(per_delete_image)
    gr_visitor.permissions.add(per_view_image)
    gr_employee.permissions.add(per_view_image)

    gr_visitor.save()
    gr_employee.save()
    #gr_customer.save()
