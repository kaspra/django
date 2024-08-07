from rest_framework import serializers
from ..models import Transaction


class RazorpayOrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    currency = serializers.CharField()


class TranscationModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['product', 'payment_id', 'order_id', 'signature', 'created_at', 'success_at', 'failed_at', 'status']
        read_only_fields = ['created_at'] 

    def get_amount(self, obj):
        return float(obj.amount)