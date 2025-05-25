# account/serializers.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from account.models import User  # Only import from account.models, not django.contrib.auth.models

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)

        # Assign default 'reader' group
        reader_group, created = Group.objects.get_or_create(name='reader')
        user.groups.add(reader_group)

        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')

        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    permissions_level = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'role', 'permissions_level', 'created_at')
        read_only_fields = ('email', 'created_at')