from django.contrib.auth.models import Permission
from rest_framework.permissions import BasePermission


class GroupUserPermissions(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_groups = user.groups.all()
        user_permissions = user.user_permissions.all()

        group_permissions = Permission.objects.filter(group__in=user_groups).distinct()
        required_permission_codenames = set(
            permission.codename for permission in user_permissions
        ) | set(permission.codename for permission in group_permissions)

        method_to_permission_action = {
            "GET": "view",
            "POST": "add",
            "PUT": "change",
            "PATCH": "change",
            "DELETE": "delete",
        }
        requested_action = method_to_permission_action.get(request.method)

        model_name = (
            getattr(view.queryset.model, "_meta", None).model_name
            if hasattr(view, "queryset") and view.queryset
            else None
        )

        if not requested_action or not model_name:
            return False

        required_permission = f"{requested_action}_{model_name}"
        if required_permission in required_permission_codenames:
            return True
        return False
