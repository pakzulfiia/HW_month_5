from rest_framework import serializers
from .models import Category, Product, Review


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = 'id name products_count'.split()
        # fields = '__all__'

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title description'.split()

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Product
        fields = 'id title description price avg_rating reviews'.split()