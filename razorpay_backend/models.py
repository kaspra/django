from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=1)  # Link to a product
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount charged
    payment_id = models.CharField(max_length=255)  # Payment ID from Razorpay
    order_id = models.CharField(max_length=255)  # Order ID from Razorpay
    signature = models.CharField(max_length=255)  # Signature from Razorpay
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of transaction
    success_at = models.DateTimeField(null=True, blank=True)  # Timestamp when transaction succeeded
    failed_at = models.DateTimeField(null=True, blank=True)  # Timestamp when transaction failed
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Status of the transaction

    def __str__(self):
        return f"Transaction {self.id} - {self.product.name}"

