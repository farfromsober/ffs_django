# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView

from .permissions import ProductPermission
from .filters import ProductsFilter, TransactionsFilter, filter_with_localization, add_distance
from .permissions import ProductPermission, TransactionPermission
from .settings import DEFAULT_CATEGORY_INDEX
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from users.models import Profile
from .serializers import ProductSerializer, ProductCreateSerializer, ProductUpdateSerializer, \
    TransactionSerializer, TransactionCreateSerializer, TransactionListSerializer
from .models import Product, Category, Transaction
from rest_framework.response import Response





class ProductViewSet(GenericViewSet):

    queryset = Product.objects.prefetch_related('images').order_by('-published_date', 'id')
    # pagination_class = PageNumberPagination
    serializer_class = ProductSerializer
    permission_classes = (ProductPermission,)
    filter_class = ProductsFilter

    def list(self, request):
        products = self.filter_class(request.query_params, queryset=self.queryset)
        products = filter_with_localization(request.query_params, products.qs)
        serializer = ProductSerializer(products, many=True)
        # añadimos la distancia a mano
        add_distance(request.query_params, serializer.data)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            category = get_object_or_404(Category, index=request.data.get('category', dict())
                                                                     .get('index', DEFAULT_CATEGORY_INDEX))
            product = serializer.save(seller=request.user.profile, category=category)
            response_serializer = ProductSerializer(product)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)  # compruebo si el usuario autenticado puede hacer GET en este product
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)  # compruebo si el usuario autenticado puede hacer PUT en este product
        serializer = ProductUpdateSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            category = get_object_or_404(Category, index=request.data.get('category', dict()).get('index'))
            seller = get_object_or_404(Profile, user=request.user)
            product = serializer.save(seller=seller, category=category)
            response_serializer = ProductSerializer(product)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)  # compruebo si el usuario autenticado puede hacer DELETE en este product
        if product.selling:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)







class TransactionViewSet(GenericViewSet):

    queryset = Transaction.objects.order_by('-date', 'id')
    #pagination_class = PageNumberPagination
    permission_classes = (TransactionPermission,)
    filter_class = TransactionsFilter

    # sobreescribimos este método para especificar distintos serializers
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TransactionSerializer
        elif self.request.method == 'POST':
            return TransactionCreateSerializer

    def list(self, request):
        transactions = self.filter_class(request.query_params, queryset=self.queryset)
        serializer = TransactionListSerializer(transactions.qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Obtenemos el buyer y el product para crear la transaction
            buyer = Profile.objects.get(pk=request.data.get('buyerId'))
            product = Product.objects.get(pk=request.data.get('productId'))

            # Creamos una instancia transaction
            transaction = Transaction(product=product, buyer=buyer)

            # Pero no la guardaremos hasta chequear los permisos
            self.check_object_permissions(request, transaction)

            if product.selling:
                # volvemos a poner el producto a la venta
                product.selling = 0
                product.save()
                # actualizamos el contador de sales
                seller = product.seller
                new_sales = seller.sales + 1
                seller.sales = new_sales
                seller.save()

            else: # no se puede crear un transaction con un producto que no está en venta
                return Response(status=status.HTTP_400_BAD_REQUEST)

            # Si OK, la guardamos y devolvemos un '201'
            transaction.save()
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):

        transaction = get_object_or_404(Transaction, pk=pk)

        # Chequeamos los permisos
        self.check_object_permissions(request, transaction)

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def update(self, request, pk):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)

        # Chequeamos los permisos
        self.check_object_permissions(request, transaction)

        product = transaction.product
        seller = transaction.product.seller
        # volvemos a poner el producto a la venta
        product.selling = 1
        product.save()
        # actualizamos el contador de sales
        new_sales = seller.sales - 1
        seller.sales = new_sales
        seller.save()

        # Si OK, la destruimos y devolvemos un '204'
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BoughtAPIView(APIView):

    def get(self, request, format=None):
        """
        Return a list of buyed products for current user.
        """

        if request.user is not None and request.user.is_active:

            all_transactions = Transaction.objects.filter(buyer__user=request.user)
            products = [transaction.product for transaction in all_transactions]
            serializer = ProductSerializer(products, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)



