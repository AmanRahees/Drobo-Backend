from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from inventory.models import *
from core.serializers.descriptors import *
from core.serializers.alternatives import _ProductSerializer, _VariantSerializer, _ImageSerializer, _AttributeSerializer
from inventory.func import *

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getDescriptors(request):
    categories = Category.objects.all()
    brands = Brands.objects.all()
    category_serializer = CategorySerializers(categories, many=True)
    brand_serializer = BrandSerializers(brands, many=True)
    data = {
        "categories": category_serializer.data,
        "brands": brand_serializer.data
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def addAlternatives(request):
    data = request.data.dict()
    variant_data, image_data = convert_data(data)
    for obj in variant_data:
        attrs = obj.pop("product_attributes")
        variant_attrs = []
        for attr in attrs:
            attr_name, attr_value = list(attr.items())[0]
            attr_pk = ProductAttributes.objects.create(attribute_name=attr_name.upper(), attribute_value=attr_value.upper())
            variant_attrs.append(attr_pk)
        obj["product_attributes"] = variant_attrs
        print(obj)
        product = Products.objects.get(id=obj["product"])
        variant_obj = ProductVariants.objects.create(
            product=product,
            price=obj["price"],
            stock=obj["stock"],
            status=obj["status"],
        )
        variant_obj.product_attributes.set(obj["product_attributes"])
        print(variant_obj)
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAlternatives(request, id):
    try:
        product = Products.objects.get(id=id)
        variants = ProductVariants.objects.filter(product=product)
        serialized_variants = []
        for variant in variants:
            attributes = ProductAttributes.objects.filter(productvariants=variant)
            images = ProductImages.objects.filter(products=variant)
            attribute_data = []
            for attribute in attributes:
                attribute_data.append({
                    attribute.attribute_name: attribute.attribute_value
                })
            
            image_data = []
            for image in images:
                image_data.append({
                    'image': image.image.url,
                    'default_img': image.default_img
                })

            serialized_variants.append({
                'variant_id': variant.id,
                'attributes': attribute_data,
                'price': variant.price,
                'stock': variant.stock,
                'images': image_data
            })
        serializer = _ProductSerializer({
            'id': product.id,
            'product_name': product.product_name,
            'description': product.description,
            'category': product.category.category_name,
            'brand': product.brand.brand_name,
            'variants': serialized_variants
        })
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)