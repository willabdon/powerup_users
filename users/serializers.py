from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers, status
from rest_framework.response import Response

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "id",
            "external_id",
        )
        model = User
        read_only_fields = ("id", "external_id")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User(**validated_data)

        try:
            validate_password(validated_data["password"], user)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        user.set_password(validated_data["password"])
        user.save()
        return user
