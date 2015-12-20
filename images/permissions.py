# -*- coding: utf-8 -*-
#__author__ = 'dregatos'

from rest_framework.permissions import BasePermission


class ImagePermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción (POST o DELETE)
        """

        # el superusuario siempre puede
        if request.user.is_superuser:
            return True

        # el cliente web pide primero con el método options lo que puede hacer, damos permiso siempre
        elif view.action == 'metadata':
            return True

        # comprobamos que el user está logeado
        else:
            return request.user.is_authenticated();

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción (GET, PUT o DELETE)/('retrieve', 'update' o 'destroy')
        sobre el object obj
        """
        # si se intenta hacer POST o DELETE,  solo un superadmin, o el 'owner' del producto pueden
        return request.user.is_superuser or request.user == obj.seller.user
