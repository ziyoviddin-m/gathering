from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Payment, Collect


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'full_name')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class CollectSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(allow_empty_file=False, use_url=True)
    collected_amount = serializers.SerializerMethodField()
    contributors_count = serializers.SerializerMethodField()
    donations = serializers.SerializerMethodField()

    class Meta:
        model = Collect
        fields = '__all__'

    def get_collected_amount(self, obj):
        return obj.collected_amount()

    def get_contributors_count(self, obj):
        return obj.contributors_count()

    def get_donations(self, obj):
        donations = obj.donations().select_related('user')
        serializer = PaymentSerializer(donations, many=True)
        return serializer.data
        


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Payment
        fields = '__all__'