from django.db import models
from django.conf import settings
from django.contrib.admin import display
from django.core.validators import MinValueValidator


class Collection(models.Model):
    title = models.CharField(max_length=150)
    col = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.title


class Promotion(models.Model):
    description = models.TextField(max_length=200)
    discount = models.FloatField()


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField()
    unit_price = models.DecimalField(
                                max_digits=6,
                                decimal_places=2,
                                validators=[MinValueValidator(1)]
                        )
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    promotions = models.ManyToManyField(Promotion, blank=True)
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['id'] 


class ProductAttribute(models.Model):
    title = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.attribute.title}  = > {self.value}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images')


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone_number = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering=['user__first_name','user__last_name']
    
    @display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions=[
            ('cancel_order','Can Cancel Order')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()


class Address(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=180)
    customer = models.ForeignKey(Customer ,on_delete=models.CASCADE)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [
            ['product', 'cart']
        ]

class Review(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.product}'