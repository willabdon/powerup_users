from rest_framework import permissions


class BelongsToUser(permissions.BasePermission):
    message = "Non authorized."

    def has_permission(self, request, view, **kwargs):
        pk = request.parser_context["kwargs"].get("pk")
        return str(request.user.id) == pk or str(request.user.external_id) == pk
