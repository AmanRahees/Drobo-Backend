from inventory.models import *

def convert_data(data):
    variant_data = []
    image_data = []
    variants = []
    images = []
    for key, value in data.items():
        if key.startswith('productVariants'):
            parts = key.split('][')
            variant_index = int(parts[0][len('productVariants['):])
            attribute_type = parts[-1].rstrip(']')
            attribute_value = value

            variant_dict = next((item for item in variants if item["id"] == str(variant_index)), None)
            if variant_dict is None:
                variant_dict = {"id": str(variant_index)}
                variants.append(variant_dict)
            if attribute_type in ['product', 'price', 'stock']:
                variant_dict[attribute_type] = int(attribute_value)
            elif attribute_type == "status":
                variant_dict[attribute_type] = attribute_value.lower() == 'true'
            else:
                variant_dict[attribute_type] = attribute_value
        elif key.startswith('productImages'):
            parts = key.split('][')
            image_index = int(parts[0][len('productImages['):])
            image_attribute = parts[1].rstrip(']')
            image_value = value
            image_dict = next((item for item in images if item["id"] == str(image_index)), None)
            if image_dict is None:
                image_dict = {"id": str(image_index)}
                images.append(image_dict)

            if image_attribute == 'image':
                image_dict['image'] = value
            else:
                image_dict[image_attribute] = value

    for variant in variants:
        attrs = []
        for key, value in variant.items():
            if key not in ['id', 'product', 'price', 'stock', 'status']:
                attrs.append({key: value})
        try:
            transformed_data = {
                'product': variant['product'],
                'product_attributes': attrs,
                'price': variant['price'],
                'stock': variant['stock'],
                'status': variant['status']
            }
            variant_data.append(transformed_data)
        except:
            pass
    print(images)
    for image in images:
        try:
            image_transformed_data = {
                'default_img': image.get('default_img').lower() == 'true',
                'image': image.get('image')
            }
            image_data.append(image_transformed_data)
        except:
            pass
    return variant_data, image_data