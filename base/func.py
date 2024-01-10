from base.serializers.products import *
from inventory.models import *

def getShopProducts():
    try:
        variants = ProductVariants.objects.all()
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