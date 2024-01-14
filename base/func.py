from base.serializers.products import *
from inventory.models import *
from django.db.models.functions import Random

def getShopProducts():
    try:
        variants = ProductVariants.objects.annotate(random_order=Random(seed=2)).order_by('random_order')
        serializer = ShopProductSerializer(variants, many=True)
        return serializer.data
    except:
        return None
    
def getProductData(pk):
    product = Products.objects.get(id=pk)
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
                'image': image.image,
                'default_img': image.default_img
            })
        serialized_variants.append({
            'variant_id': variant.id,
            'attributes': attribute_data,
            'price': variant.price,
            'stock': variant.stock,
            'images': image_data
        })
    serializer = ProductViewSerializer({
        'id': product.id,
        'product_name': product.product_name,
        'description': product.description,
        'category': product.category.category_name,
        'brand': product.brand,
        'variants': serialized_variants
    })
    return serializer.data

def getVariantData(pk):
    variant_data = {}
    variant = ProductVariants.objects.get(pk=pk)
    variant_data["id"] = variant.id
    variant_data["product_name"] = variant.product.product_name
    for i in variant.product_attributes.all():
        variant_data[i.attribute_name] = i.attribute_value
    variant_data["price"] = variant.price
    variant_data["stock"] = variant.stock
    obj_variants = []
    product = Products.objects.get(id=variant.product.id)
    variants = ProductVariants.objects.filter(product=product)
    for i in variants:
        variants_data = {}
        variants_data["id"] = i.id
        variants_data["product_name"] = i.product.product_name
        for attrs in i.product_attributes.all():
            variants_data[attrs.attribute_name] = attrs.attribute_value
        variants_data["price"] = i.price
        variants_data["stock"] = i.stock
        for img in ProductImages.objects.filter(products=i):
            if img.default_img == True:
                variants_data['image'] = img.image.url
        obj_variants.append(variants_data)
    print(obj_variants)
    unique = []
    for item in obj_variants:
        unique.append(item['COLOR'])
    print(set(unique))
    return variant_data