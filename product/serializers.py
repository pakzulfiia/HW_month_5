from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError



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
        
class CategoryValidateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    class Meta:
        model = Category
        fields = ("name",)


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title description'.split()

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductValidateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = (
            "title",
            "description",
            "price",
            "category",
        )

    # def validate_category_id(self, category_id):
    #     try:
    #         Category.objects.get(id=category_id)
    #     except Category.DoesNotExist:
    #         raise ValidationError('Category is not found')
    #     return category_id


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewValidateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    
    class Meta:
        model = Review
        fields = (
            'text',
            'stars',
            'product'
        )

    # def validate_product_id(self, product_id):
    #     try:
    #         Product.objects.get(id=product_id)
    #     except Product.DoesNotExist:
    #         raise ValidationError('Product is not found!')
    #     return product_id


class ProductReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Product
        fields = 'id title description price avg_rating reviews'.split()

