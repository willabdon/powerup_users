from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserCreateRetrieveSerializer, UserUpdateSerializer
from users.permissions import BelongsToUser


class UserCreateUpdateRetrieveViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Create, Update and Retrieve users.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "update" or self.action == "partial_update":
            return UserUpdateSerializer
        return UserCreateRetrieveSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated, BelongsToUser]

        return super(UserCreateUpdateRetrieveViewSet, self).get_permissions()

    def get_object(self, **kwargs):
        _id = self.kwargs.get("pk")

        try:
            return self.queryset.get(id=_id)
        except:
            pass

        try:
            return self.queryset.get(external_id=_id)
        except:
            pass

        return None

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
