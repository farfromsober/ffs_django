# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):

        # crear un usuario, todos tienen permiso
        if view.action == "create":
            return True
        # si no es POST, el superusuario siempre puede
        elif request.user.is_superuser:
            return True
        # para los GET al detalle, se delega la decision a has_object_permissions
        elif view.action in ['retrieve', 'update', 'destroy']:
            return True
        else:
            # otros GET a /api/1.0/users/ no se permiten
            return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción (GET, PUT o DELETE)
        sobre el object obj
        """
        # si es superadmin, o el usuario autenticado intenta
        # hacer GET, PUT o DELETE sobre su mismo perfil
        return request.user.is_superuser or request.user == obj
