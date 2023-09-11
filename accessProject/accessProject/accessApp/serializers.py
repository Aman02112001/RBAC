# your_app_name/serializers.py
from rest_framework import serializers
from .models import Role, API, CustomUser

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = API
        fields = ('id', 'user', 'name', 'url', 'endpoint', 'description', 'mapped_users')

class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role_name = validated_data.pop('role')
        try:
            role = Role.objects.get(name=role_name)
            user = CustomUser.objects.create_user(**validated_data)
            user.role = role_name
            user.save()
        except Role.DoesNotExist:
            raise serializers.ValidationError(f"Role '{role_name}' does not exist.")
        return user
