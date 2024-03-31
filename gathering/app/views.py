from rest_framework import generics
from django.core.cache import cache
from .serializers import CollectSerializer, PaymentSerializer
from .models import Collect, Payment
from rest_framework.response import Response



class CachedListCreateAPIView(generics.ListCreateAPIView):
    cache_timeout = 60
    cache_key_prefix = None

    def list(self, request, *args, **kwargs):
        key = self.get_cache_key('list')
        data = cache.get(key)
        if not data:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(key, data, timeout=self.cache_timeout)
        return Response(data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.invalidate_cache('list')
        return response

    def get_cache_key(self, action):
        if self.cache_key_prefix is None:
            raise NotImplementedError("Необходимо установить атрибут cache_key_prefix")
        return f'{self.cache_key_prefix}_{action}'

    def invalidate_cache(self, action):
        cache.delete(self.get_cache_key(action))


class CachedRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    cache_timeout = 60
    cache_key_prefix = None

    def retrieve(self, request, *args, **kwargs):
        key = self.get_cache_key(kwargs['pk'])
        data = cache.get(key)
        if not data:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            cache.set(key, data, timeout=self.cache_timeout)
        return Response(data)

    def update(self, request, *args, **kwargs):
        key = self.get_cache_key(kwargs['pk'])
        cache.delete(key)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        key = self.get_cache_key(kwargs['pk'])
        cache.delete(key)
        self.invalidate_cache('list')
        return super().destroy(request, *args, **kwargs)

    def get_cache_key(self, pk_or_action):
        if self.cache_key_prefix is None:
            raise NotImplementedError("Необходимо установить атрибут cache_key_prefix")
        return f'{self.cache_key_prefix}_{pk_or_action}'

    def invalidate_cache(self, action):
        cache.delete(self.get_cache_key(action))


class CollectAPIList(CachedListCreateAPIView):
    queryset = Collect.objects.prefetch_related('payments', 'author').all()
    serializer_class = CollectSerializer
    cache_key_prefix = 'collect_list'


class CollectAPIUpdate(CachedRetrieveUpdateDestroyAPIView):
    queryset = Collect.objects.select_related('author').prefetch_related('payments').all()
    serializer_class = CollectSerializer
    cache_key_prefix = 'collect'

class PaymentAPIList(CachedListCreateAPIView):
    queryset = Payment.objects.select_related('user', 'collect').all()
    serializer_class = PaymentSerializer
    cache_key_prefix = 'payment_list'


class PaymentAPIDelete(CachedRetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.select_related('user').all()
    serializer_class = PaymentSerializer
    cache_key_prefix = 'payment'
