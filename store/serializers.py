from rest_framework import serializers
from .models import *

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','name','description']
    
    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','product_count']
    product_count=serializers.IntegerField(read_only=True)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','slug','description','collection','unit_price','inventory']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','product','quantity', 'total_price']
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    
    def get_total_price(self, cartitem):
        return cartitem.product.unit_price * cartitem.quantity


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['id','items','total_price']
    items=CartItemSerializer(many=True, read_only=True)
    total_price=serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
    product_id=serializers.IntegerField()

    def save(self, **kwargs):
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        cart_id=self.context['cart_id']

        try:
            cartitem=CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance=cartitem
        except:
            self.instance=CartItem.objects.create(cart_id=cart_id, **self.validated_data)

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
    product_id=serializers.IntegerField()

    def save(self, **kwargs):
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        cart_id=self.context['cart_id']

        try:
            cartitem=CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance=cartitem
        except:
            self.instance=CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['id','user_id','phone_number','birth_date','membership']
    user_id=serializers.IntegerField(read_only=True)