from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import (CategoryListSerializer, 
                          CategoryDetailSerializer, 
                          CategoryValidateSerializer,
                          ProductDetailSerializer, 
                          ProductReviewSerializer,
                          ProductListSerializer, 
                          ProductValidateSerializer,
                          ReviewDetailSerializer, 
                          ReviewListSerializer,
                          ReviewValidateSerializer)
from rest_framework import status
from django.db.models import Count, Avg
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination



# # Create your views here.
class CustomTotalPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    pagination_class = CustomTotalPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CategoryValidateSerializer
        return CategoryListSerializer

    def create(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            category = serializer.save()

        return Response(CategoryDetailSerializer(category).data,status=status.HTTP_201_CREATED)
    
# @api_view(http_method_names=['GET', 'POST'])
# def category_list_api_view(request):
#     if request.method == 'GET':
#         categories = Category.objects.annotate(products_count=Count('products'))
#         data = CategoryListSerializer(categories, many=True).data

#         return Response(data=data)
#     elif request.method == 'POST':
#         serializer = CategoryValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
        
#         name = serializer.validated_data.get('name')

#         with transaction.atomic():
#             category = Category.objects.create(
#             name=name
#             )
#             category.save()

#         # 3 step: return response (status, data)
#         return Response(status=status.HTTP_201_CREATED,
#                         data=CategoryDetailSerializer(category).data)


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    pagination_class = CustomTotalPagination

    def get_object(self):
        try:
            return Category.objects.get(id=self.kwargs["id"])
        except Category.DoesNotExist:
            return Response(data={'error': 'category not found!'},
                        status=status.HTTP_404_NOT_FOUND)
            
# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def category_detail_api_view(request, id):
#     try:
#         category = Category.objects.get(id=id)
#     except Category.DoesNotExist:
#         return Response(data={'error': 'category not found!'},
#                         status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         data = CategoryDetailSerializer(category, many=False).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = CategoryValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         category.name = request.data.get('name')
#         category.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data=CategoryDetailSerializer(category).data)
#     elif request.method == 'DELETE':
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    pagination_class = CustomTotalPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductValidateSerializer
        return ProductListSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            product = serializer.save()

        return Response(ProductDetailSerializer(product).data,status=status.HTTP_201_CREATED)

# @api_view(http_method_names=['GET', 'POST'])
# def product_list_api_view(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         data = ProductListSerializer(products, many=True).data

#         return  Response(
#             data=data
#         )
#     elif request.method == 'POST':
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
        
#         title = serializer.validated_data.get('title')
#         description = serializer.validated_data.get('description')
#         price = serializer.validated_data.get('price')
#         category_id = serializer.validated_data.get('category_id')
        
#         with transaction.atomic():
#             product = Product.objects.create(
#                 title=title,
#                 description=description,
#                 price=price,
#                 category_id=category_id
#             ) 
#             product.save()

#         return Response(status=status.HTTP_201_CREATED,
#                         data=ProductDetailSerializer(product).data)


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    pagination_class = CustomTotalPagination

    def get_object(self):
        try:
            return Product.objects.get(id=self.kwargs["id"])
        except Product.DoesNotExist:
            return Response(data={'error': 'product not found!'},
                        status=status.HTTP_404_NOT_FOUND)

# @api_view(http_method_names=['GET', 'PUT', 'DELETE'])
# def product_detail_api_view(request, id):
#     try:
#         product = Product.objects.get(id=id)
#     except Product.DoesNotExist:
#         return Response(data={'error': 'product not found!'},
#                         status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         data = ProductDetailSerializer(product, many=False).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = ProductValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         product.title = request.data.get('title')
#         product.description = request.data.get('description')
#         product.price = request.data.get('price')
#         product.category_id = request.data.get('category_id')
#         product.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ProductDetailSerializer(product).data)
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    pagination_class = CustomTotalPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewValidateSerializer
        return ReviewListSerializer

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            review = serializer.save()

        return Response(ReviewDetailSerializer(review).data,status=status.HTTP_201_CREATED)


# @api_view(http_method_names=['GET', 'POST'])
# def review_list_api_view(request):
#     if request.method == 'GET':
#         reviews = Review.objects.all()
#         data = ReviewListSerializer(reviews, many=True).data

#         return  Response(
#             data=data
#         )
#     elif request.method == 'POST':
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)
        
#         text = serializer.validated_data.get('text')
#         stars = serializer.validated_data.get('stars')
#         product_id = serializer.validated_data.get('product_id')

#         with transaction.atomic():
#             review = Review.objects.create(
#                 text=text,
#                 stars=stars,
#                 product_id=product_id
#             )
#             review.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ReviewDetailSerializer(review).data)

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    pagination_class = CustomTotalPagination

    def get_object(self):
        try:
            return Review.objects.get(id=self.kwargs["id"])
        except Review.DoesNotExist:
            return Response(data={'error': 'review not found!'},
                        status=status.HTTP_404_NOT_FOUND)

# @api_view(http_method_names=['GET','PUT', 'DELETE'])
# def review_detail_api_view(request, id):
#     try:
#         review = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response(data={'error': 'review not found!'},
#                         status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         data = ReviewDetailSerializer(review, many=False).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = ReviewValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         review.text = request.data.get('text')
#         review.stars = request.data.get('stars')
#         review.product_id = request.data.get('product_id')
#         review.save()
#         return Response(status=status.HTTP_201_CREATED,
#                         data=ReviewDetailSerializer(review).data)
#     elif request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ProductReviewsAPIView(ListAPIView):
    queryset = Product.objects.annotate(avg_rating=Avg('reviews__stars')).prefetch_related('reviews').all()
    serializer_class = ProductReviewSerializer
    
# @api_view(http_method_names=['GET'])
# def product_reviews_api_view(request):
#     products = Product.objects.annotate(avg_rating=Avg('reviews__stars')).prefetch_related('reviews').all()
#     data = ProductReviewSerializer(products, many=True).data

#     return Response(data=data)