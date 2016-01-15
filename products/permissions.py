# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class ProductPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción (GET, POST, PUT o DELETE)
        """

        # el superusuario siempre puede
        if request.user.is_superuser:
            return True

        # si es un 'list'/'retrieve', solo pueden usuarios autenticados.
        # Para 'retrieve' de un producto, pasamos la responsabilidad a 'has_object_permission'
        elif view.action in ['list', 'retrieve']:
            return request.user.is_authenticated()

        #si es un 'create' de un producto, solo pueden usuarios autenticados
        elif view.action == 'create':
            return request.user.is_authenticated()

        # si es un 'update'/'destroy' de un producto, pasamos la responsabilidad a 'has_object_permission'
        elif view.action in ['update', 'destroy']:
            return True

        # el cliente web pide primero con el método options lo que puede hacer, damos permiso siempre
        elif view.action == 'metadata':
            return True

        # resto de casos
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción (GET, PUT o DELETE)/('retrieve', 'update' o 'destroy')
        sobre el object obj
        """
        # si se intenta hacer 'GET', solo los usuarios autenticados pueden
        # si se intenta hacer PUT o DELETE,  solo un superadmin, o el 'seller' del producto pueden
        return True if view.action == 'retrieve' else request.user.is_superuser or request.user == obj.seller.user

class TransactionPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción (GET, POST, PUT o DELETE)
        """

        # el superusuario siempre puede
        if request.user.is_superuser:
            return True

        # el usuario tendrá que estar autenticado, pero aún así pasaremos
        # la responsabilidad al 'has_object_permission' para comprobar que
        # el request.user == user[buyerId]
        elif view.action in ['list', 'retrieve', 'create', 'update', 'destroy']:
            return request.user.is_authenticated()

        # el cliente web pide primero con el método options lo que puede hacer, damos permiso siempre
        elif view.action == 'metadata':
            return True

        # resto de casos
        else:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Define si el usuario autenticado en request.user tiene
        permiso para realizar la acción sobre el object obj
        """
        if view.action == 'create':  # el usuario es el 'buyer' y NO es dueño del producto
            return request.user.is_superuser or request.user == obj.buyer.user and request.user != obj.product.seller.user
        elif view.action in ['update', 'destroy']: # el usuario es dueño del producto involucrado en la transaction
            return request.user.is_superuser or request.user == obj.product.seller.user
        elif view.action in ['list', 'retrieve']:  # cualquiera usuario autenticado puede ver una transaction
            return True
        else:
            return False