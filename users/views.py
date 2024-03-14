from rest_framework import mixins, viewsets
from rest_framework.response import Response

from users.models import User
from users.serializers import UserCreateSerializer


class UserCreateUpdateRetrieveViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Create, Update and Retrieve users.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserCreateSerializer
