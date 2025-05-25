# account/management/commands/create_test_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from account.models import User


class Command(BaseCommand):
    help = 'Create test users for each role'

    def handle(self, *args, **options):
        # Get groups
        try:
            reader_group = Group.objects.get(name='reader')
            creator_group = Group.objects.get(name='creator')
            owner_group = Group.objects.get(name='owner')
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Groups not found. Run create_groups command first.')
            )
            return

        # Create test users
        users_data = [
            {
                'email': 'reader@example.com',
                'username': 'reader',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Reader',
                'group': reader_group
            },
            {
                'email': 'creator@example.com',
                'username': 'creator',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Creator',
                'group': creator_group
            },
            {
                'email': 'owner@example.com',
                'username': 'owner',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Owner',
                'group': owner_group
            }
        ]

        for user_data in users_data:
            group = user_data.pop('group')

            # Check if user already exists
            if User.objects.filter(email=user_data['email']).exists():
                self.stdout.write(f"User {user_data['email']} already exists")
                continue

            # Create user
            user = User.objects.create_user(**user_data)
            user.groups.add(group)

            self.stdout.write(
                self.style.SUCCESS(f"Created {group.name}: {user.email}")
            )

        self.stdout.write(
            self.style.SUCCESS('Test users created successfully!')
        )