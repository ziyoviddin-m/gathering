from rest_framework import generics
from django.core.cache import cache
from .serializers import CollectSerializer, PaymentSerializer
from .models import Collect, Payment
from rest_framework.response import Response



class CollectAPIList(generics.ListCreateAPIView):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer

    def list(self, request, *args, **kwargs):
        key = 'collect_list'
        data = cache.get(key)
        if not data:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(key, data, timeout=60)
        return Response(data)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete('collect_list')
        return response


class CollectAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer

    def retrieve(self, request, *args, **kwargs):
        key = f'collect_{kwargs["pk"]}'
        data = cache.get(key)
        if not data:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            cache.set(key, data, timeout=60)
        return Response(data)

    def update(self, request, *args, **kwargs):
        key = f'collect_{kwargs["pk"]}'
        cache.delete(key)
        return super().update(request, *args, **kwargs)


class CollectAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer

    def destroy(self, request, *args, **kwargs):
        key = f'collect_{kwargs["pk"]}'
        cache.delete(key) 
        return super().destroy(request, *args, **kwargs)


class PaymentAPIList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request, *args, **kwargs):
        key = 'payment_list'
        data = cache.get(key)
        if not data:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(key, data, timeout=60)
        return Response(data)

    def create(self, request, *args, **kwargs):
        cache.delete('payment_list') 
        return super().create(request, *args, **kwargs)


class PaymentAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def retrieve(self, request, *args, **kwargs):
        key = f'payment_{kwargs["pk"]}'
        data = cache.get(key)
        if not data:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            cache.set(key, data, timeout=60)
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        key = f'payment_{kwargs["pk"]}'
        cache.delete(key)
        cache.delete('payment_list')
        return super().destroy(request, *args, **kwargs)

