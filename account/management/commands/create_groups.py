# account/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create user groups with permissions'

    def handle(self, *args, **options):
        # Create groups
        reader_group, created = Group.objects.get_or_create(name='reader')
        if created:
            self.stdout.write(f'Created group: reader')

        creator_group, created = Group.objects.get_or_create(name='creator')
        if created:
            self.stdout.write(f'Created group: creator')

        owner_group, created = Group.objects.get_or_create(name='owner')
        if created:
            self.stdout.write(f'Created group: owner')

        # Get permissions
        permissions = Permission.objects.all()

        # Assign permissions to groups
        # Reader: only view permissions
        view_permissions = permissions.filter(codename__startswith='view_')
        reader_group.permissions.set(view_permissions)
        self.stdout.write(f'Assigned {view_permissions.count()} view permissions to readers')

        # Creator: view, add and change permissions
        creator_permissions = permissions.filter(
            codename__startswith=('view_', 'add_', 'change_')
        )
        creator_group.permissions.set(creator_permissions)
        self.stdout.write(f'Assigned {creator_permissions.count()} permissions to creators')

        # Owner: all permissions
        owner_group.permissions.set(permissions)
        self.stdout.write(f'Assigned {permissions.count()} permissions to owners')

        self.stdout.write(
            self.style.SUCCESS('Successfully created groups and assigned permissions')
        )