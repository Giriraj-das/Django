from rest_framework.permissions import BasePermission

from ads.models import Ad, User, Selection


class SelectionUpdatePermission(BasePermission):
    message = 'You can not change or delete this selection'

    def has_permission(self, request, view):
        try:
            selection = Selection.objects.get(pk=view.kwargs['pk'])
        except Selection.DoesNotExist:
            return False

        if selection.owner_id == request.user.id:
            return True
        elif request.user.role != User.Roles.MEMBER:
            return True
        else:
            return False


class AdUpdateDeletePermission(BasePermission):
    message = 'You can not change or delete this ad'

    def has_permission(self, request, view):
        try:
            ad = Ad.objects.get(pk=view.kwargs['pk'])
        except Selection.DoesNotExist:
            return False

        if ad.author_id == request.user.id:
            return True
        elif request.user.role == User.Roles.ADMIN:
            return True
        elif request.user.role == User.Roles.MODERATOR:
            return True
        else:
            return False
