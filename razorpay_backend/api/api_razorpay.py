from rest_framework.views import APIView
from rest_framework import status
from ..models import Product
from django.utils import timezone  
from .razorpay_serializers import RazorpayOrderSerializer, TranscationModelSerializer
from razorpay_backend.api.razorpay.main import RazorpayClient
from rest_framework.response import Response

rz_client = RazorpayClient()

class RazorpayOrderAPIView(APIView):
    """This API will create an order"""
    
    def post(self, request):
        razorpay_order_serializer = RazorpayOrderSerializer(data=request.data)
        if razorpay_order_serializer.is_valid():
            product_id = razorpay_order_serializer.validated_data.get("product_id")
            try:
                product = Product.objects.get(id=product_id)
                amount = float(product.amount)  # Assuming 'amount' is a field in your Product model
            except Product.DoesNotExist:
                return Response({
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Product not found"
                }, status=status.HTTP_404_NOT_FOUND)

            order_response = rz_client.create_order(
                amount=amount,
                currency=razorpay_order_serializer.validated_data.get("currency")
            )
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order_response
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": razorpay_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TransactionAPIView(APIView):
    """This API will complete order and save the 
    transaction"""
    
    def post(self, request):
        transaction_serializer = TranscationModelSerializer(data=request.data)
        if transaction_serializer.is_valid():
            data = transaction_serializer.validated_data
            product_id = data.get("product")

            try:
                rz_client.verify_payment_signature(
                    razorpay_payment_id=data.get("payment_id"),
                    razorpay_order_id=data.get("order_id"),
                    razorpay_signature=data.get("signature")
                )
                
                product = Product.objects.get(id=product_id)
                amount = float(product.amount)  

                transaction = Transaction.objects.create(
                    product=product,
                    amount=amount,
                    payment_id=data.get("payment_id"),
                    order_id=data.get("order_id"),
                    signature=data.get("signature"),
                    status='success',  # Update this based on actual success/failure logic
                    success_at=datetime.now()  # Set to the current time for successful transactions
                )
                
                response = {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "transaction created",
                    "data": TranscationModelSerializer(transaction).data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                # Update the transaction status to failed and set failed_at
                transaction = Transaction.objects.create(
                    product=product,
                    amount=amount,
                    payment_id=data.get("payment_id"),
                    order_id=data.get("order_id"),
                    signature=data.get("signature"),
                    status='failed',
                    failed_at=datetime.now()  # Set to the current time for failed transactions
                )
                response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "transaction verification failed",
                    "error": str(e)
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": transaction_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)