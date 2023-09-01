from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from accounts.models import User, Address
from order.models import Order, OrderItems
from api.serializers import UserSerializer, AddressSerializer, OrderSerializers, OrderItemSerializers


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()

    def list(self, request):
        serializer_data = UserSerializer(instance=self.queryset, many=True)
        return Response(data= serializer_data.data)

    def create(self, request):
        serializer_data = UserSerializer(data=request.POST)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer_data = UserSerializer(instance=user)
        return Response(data= serializer_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        user.is_active = False
        user.save()
        return Response({'result': 'user deactivated now...'}, status=status.HTTP_200_OK)


class AddressViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()

    def list(self, request):
        serializer_data = AddressSerializer(instance=self.queryset.filter(user=request.user), many=True)
        return Response(data= serializer_data.data)

    def create(self, request):
        serializer_data = AddressSerializer(data=request.POST)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        serializer_data = AddressSerializer(instance=user)
        return Response(data= serializer_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        order = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        serializer_data = AddressSerializer(instance=order, data=request.POST, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        address = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        address.delete()
        address.save()
        return Response({'result': 'Address deleted...'}, status=status.HTTP_200_OK)
    

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()

    def list(self, request):
        serializer_data = OrderSerializers(instance=self.queryset.filter(user=request.user), many=True)
        return Response(data= serializer_data.data)

    def create(self, request):
        serializer_data = OrderSerializers(data=request.POST)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        serializer_data = OrderSerializers(instance=user)
        return Response(data= serializer_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        order = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        serializer_data = OrderSerializers(instance=order, data=request.POST, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        order.is_active = False
        order.save()
        return Response({'result': 'order deleted now...'}, status=status.HTTP_200_OK)
    

class OrderItemViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = OrderItems.objects.all()

    def list(self, request):
        serializer_data = OrderItemSerializers(instance=self.queryset.filter(user=request.user), many=True)
        return Response(data= serializer_data.data)

    def create(self, request):
        serializer_data = OrderItemSerializers(data=request.POST)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        serializer_data = OrderItemSerializers(instance=user)
        return Response(data= serializer_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        order = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        serializer_data = OrderItemSerializers(instance=order, data=request.POST, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        order.is_active = False
        order.save()
        return Response({'result': 'order deleted now...'}, status=status.HTTP_200_OK)